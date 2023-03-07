/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:55:10
 * @LastEditTime: 2023-03-07 23:14:18
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1i/B3i BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.hpp
 */

#ifndef SIGNALPROCESS_BPSK_B1ISIM_HPP_
#define SIGNALPROCESS_BPSK_B1ISIM_HPP_

#include "../util/dataSource.hpp"
#include "../util/satInfo.hpp"

namespace signalProcess {

// ---------------
//  SIGNAL PARAMS
// ---------------

#define B1I_CARR_FREQ         1561.098e6          //< B1I Carrier Frequency
#define B1I_CARR_LAMBDA       0.19203948631027648 //< B1I Carrier Wavelength
#define B1I_RANGING_CODE_RATE 2.046e6
#define B1I_DATA_RATE         50
#define B1I_NH_RATE           1000

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
#define SIMULATION_TIME 300
#define SIM_UPDATE_STEP 0.1 //< Simulation Update Step for pesudo range

// -------------------
//  CHANNEL SIMULATION
// -------------------

class b1iChannel {
private:
    signalProcess::b1ISatInfo  satInfo;
    signalProcess::bDataSource frameData;
    signalProcess::bDataSource rangingCode;
    signalProcess::bDataSource nhCode;
    signalProcess::fDataSource delay;
    signalProcess::fDataSource refDelay;
    signalProcess::fDataSource elevation;
    unsigned int               carrPhase;
    int                        carrPhaseStep;

public:
    /**
     * @brief Construct a new b1i Channel object
     * 
     * @param sat_info 
     * @param data_src 
     */
    b1iChannel(const signalProcess::b1ISatInfo& sat_info);
};
} // namespace signalProcess

#endif