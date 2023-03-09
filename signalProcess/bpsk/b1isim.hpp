/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:55:10
 * @LastEditTime: 2023-03-09 12:21:59
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1i/B3i BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.hpp
 */

#ifndef SIGNALPROCESS_BPSK_B1ISIM_HPP_
#define SIGNALPROCESS_BPSK_B1ISIM_HPP_

#include "../util/dataSource.hpp"
#include "../util/satInfo.hpp"
#include "../util/constants.hpp"
#include <tuple>

namespace signalProcess {

// ---------------
//  SIGNAL PARAMS
// ---------------

#define B1I_CARR_FREQ         1561.098e6          //< B1I Carrier Frequency
#define B1I_CARR_LAMBDA       0.19203948631027648 //< B1I Carrier Wavelength
#define B1I_RANGING_CODE_RATE 2.046e6
#define B1I_DATA_RATE         50
#define B1I_NH_RATE           1000
#define LIGHT_SPEED           299792458
#define CARR_PERIOD_PER_CHIP  (2.046e6 / 1561.098e6)

// ---------------
//   CODE PARAMS
// ---------------

#define B1I_NH_CODE_LEN      20
#define B1I_RANGING_CODE_LEN 2046
#define B1I_NH_CODE          "04d4e"

// -------------------
//  SIMULATION PARAMS
// -------------------

#define MAX_CHANNEL_NUM 4
#define SIMULATION_TIME 120
#define SIM_UPDATE_STEP 0.1 //< Simulation Update Step for pesudo range
#define SAMPLE_FREQ     4092000 //< Sample Frequency, 2.046e6
#define ITER_LENGTH     409200  // 2046000 / 10

// -------------------
//  CHANNEL SIMULATION
// -------------------

/**
 * @brief B1I Channel Simulation
 * 在这一步实现一个更高的抽象，减少后面调用部分的复杂度。
 * 
 */
class b1iChannel {
private:
    signalProcess::b1ISatInfo  satInfo;     //< Satellite Information
    signalProcess::bDataSource frameData;   //< Frame Data
    signalProcess::bDataSource rangingCode; //< Satellite PRN Code
    signalProcess::bDataSource nhCode;      //< NH Sparse Code
    signalProcess::fDataSource delay;       //< The delay caused by pesudorange
    signalProcess::fDataSource
        elevation; //< Elevation Angle, for Gain calculation

    double       prevDelay;     //< Previous Delay, for phase update.
    double       refDelay;      //< Reference Delay, caused by the
                                // pesudorange to ECEF(0,0,0)
    unsigned int carrPhase;     //< Carrier Phase
    int          carrPhaseStep; //< Carrier phase step for simulation
    double       codePhase;     //< Code Phase
    double       delt;          //< sampling interval
    int          gain;          //< Gain for the channel
    double       carrFreq;      //< Carrier Frequency, for phase update
    double       codeFreq;      //< Code Frequency, for phase update
    double       iterTimes;     //< Iteration Times, for phase update
    int          iterIdx;       //< Iteration Index, trigging update
    int          nhBitIdx;      //< NH Bit Index

    /**
     * @brief Recalculate the code phase.
     * 
     */
    void recalculateCodePhase();
    /**
     * @brief Update the channel status every sample interval.
     * This function will update the carrier phase and recalculate gain.
     */
    void updateChannelStatus();

public:
    /**
     * @brief Construct a new b1i Channel object
     * 
     * @param sat_info 
     * @param data_src 
     */
    b1iChannel(const signalProcess::b1ISatInfo& sat_info);
    b1iChannel(){};
    ~b1iChannel(){};
    /**
     * @brief Get the I/Q Data 
     * 
     * @return std::tuple<double, double>, which is a I/Q data tuple
     */
    std::tuple<int, int> getNextData();
};
} // namespace signalProcess

#endif