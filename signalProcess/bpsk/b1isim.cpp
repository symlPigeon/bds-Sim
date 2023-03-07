/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:54:48
 * @LastEditTime: 2023-03-07 23:19:35
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1I/B3I BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.cpp
 */

#include "b1isim.hpp"
#include <cmath>

namespace signalProcess {

b1iChannel::b1iChannel(const signalProcess::b1ISatInfo& sat_info)
    : satInfo(sat_info) {
    frameData   = signalProcess::bDataSource(sat_info.getData(), 3);
    rangingCode = signalProcess::bDataSource(sat_info.getPrn(), 3);
    nhCode      = signalProcess::bDataSource(B1I_NH_CODE, 4);
    delay       = signalProcess::fDataSource(sat_info.getDelay());
    refDelay    = signalProcess::fDataSource(sat_info.getRefDelay());
    elevation   = signalProcess::fDataSource(sat_info.getElevation());
}

} // namespace signalProcess