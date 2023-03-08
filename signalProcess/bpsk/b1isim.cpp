/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:54:48
 * @LastEditTime: 2023-03-08 18:23:58
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1I/B3I BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.cpp
 */

#include "b1isim.hpp"
#include <cmath>

namespace signalProcess {

b1iChannel::b1iChannel(const signalProcess::b1ISatInfo& sat_info)
    : satInfo(sat_info),
      frameData(signalProcess::bDataSource(sat_info.getData(), 4)),
      rangingCode(signalProcess::bDataSource(sat_info.getPrn(), 3)),
      nhCode(signalProcess::bDataSource(B1I_NH_CODE, 4)),
      delay(signalProcess::fDataSource(sat_info.getDelay())),
      elevation(signalProcess::fDataSource(sat_info.getElevation())),
      refDelay(sat_info.getRefDelay()),
      delt(1. / SAMPLE_FREQ),
      iterTimes(0),
      iterIdx(ITER_LENGTH),
      nhBitIdx(0) {
    // Set the initial phase
    double init_r     = delay.getDataAtIdx(0);
    double init_rref  = refDelay;
    double init_phase = (init_rref * 2 - init_r) * B1I_CARR_FREQ;
    init_phase        = init_phase - floor(init_phase);
    carrPhase         = static_cast<unsigned int>(init_phase * 512 * 65536);
    prevDelay         = init_r; //< just update the prev_delay.
}

void b1iChannel::recalculateCodePhase() {
    // 每次经过SIM_UPDATE_STEP时间，我们需要更新一次伪距，以降低卫星运动产生的误差。
    // t_s = TOW + (30w + b) * 0.02 + NHB * 0.001 + CP / 2046 * 0.001
    // 其中t_s为卫星发射时间，TOW为帧中记录的时间也就是帧起始时间，w为接收到的完整的字数
    // b为当前正在接收的字中已接收的比特数，NHB为正在接收的比特中接收到的完整的NH code的比特数
    // CP为正在接收的测距码的相位

    // Update the delay.
    double curr_delay = this->delay.getData();
    // calculate the rho changing rate in previous step(0.1s)
    // NOTE: the first step should be incorrect, maybe we just ignore it.
    double rho_rate =
        (curr_delay - this->prevDelay) * LIGHT_SPEED / SIM_UPDATE_STEP;
    // update the carrier and code frequency
    this->carrFreq = -rho_rate / B1I_CARR_LAMBDA;
    this->codeFreq = B1I_RANGING_CODE_RATE + carrFreq * CARR_PERIOD_PER_CHIP;
    // calculate the continue time
    // plus 6 to make sure the ms is positive
    double ms       = (iterTimes * SIM_UPDATE_STEP + 6 - curr_delay) * 1000;
    int    ims      = static_cast<int>(ms);
    this->codePhase = (ms - ims) * B1I_RANGING_CODE_LEN;

    // Calculate the index of frame.
    int startWord  = ims / 600;
    int startBit   = (ims % 600) / 20;
    this->nhBitIdx = (ims % 20);

    // Set the index of data source
    this->frameData.setIdx(startWord * 30 + startBit);

    // Update the prev_delay
    this->prevDelay = curr_delay;
    this->delay.next();

    // reset the iterIdx
    this->iterIdx = 0;
}

void b1iChannel::updateChannelStatus() {
    // update simulation iter times
    this->iterTimes += SIM_UPDATE_STEP;
    // recalculate code phase, this is important for pesudorange localation
    this->recalculateCodePhase();
    this->carrPhaseStep =
        static_cast<int>(std::round(512 * 65536 * this->carrFreq * this->delt));
    // Calculate the path loss. We use pesudo range instead of real range, just for convenience.
    double path_loss = 20200000.0 / (this->prevDelay * LIGHT_SPEED);
    double elevation = this->elevation.getData();
    this->elevation.next();
    // Calculate the signal gain
    int ibs = static_cast<int>((90 - elevation) / 5.);
    this->gain =
        static_cast<int>(signalProcess::ant_pat[ibs] * path_loss * 128.0);
}

std::tuple<int, int> b1iChannel::getNextData() {
    if (this->iterIdx == ITER_LENGTH) {
        this->updateChannelStatus();
    }
    int iTable = (int)(this->carrPhase >> 16) & 0x1ff;
    // get next ranging code bit
    int code_bit =
        this->rangingCode.getBitAtIdx((int)(this->codePhase)) * 2 - 1;
    // get next nh code bit
    int nh_bit = this->nhCode.getBitAtIdx(this->nhBitIdx) * 2 - 1;
    // get next data bit
    int data_bit = this->frameData.getBit() * 2 - 1;

    int ip = data_bit * code_bit * nh_bit * signalProcess::cosTable512[iTable]
             * this->gain;
    int qp = data_bit * code_bit * nh_bit * signalProcess::sinTable512[iTable]
             * this->gain;

    this->codePhase += this->codeFreq * delt;
    if (this->codePhase >= B1I_RANGING_CODE_LEN) {
        this->codePhase -= B1I_RANGING_CODE_LEN;
        // this ranging code period is over, goto next nhCode bit.
        this->nhBitIdx++;
        if (this->nhBitIdx == B1I_NH_CODE_LEN) {
            // all the nh code bits are over, goto next frame data bit.
            this->nhBitIdx = 0;
            this->frameData.next();
        }
        this->carrPhase += this->carrPhaseStep;
    }
    this->iterIdx++;
    return std::make_tuple(ip, qp);
}

} // namespace signalProcess