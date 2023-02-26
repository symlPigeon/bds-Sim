/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:55:10
 * @LastEditTime: 2023-02-26 11:02:18
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1i/B3i BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.hpp
 */

#ifndef SIGNALPROCESS_BPSK_B1ISIM_HPP_
#define SIGNALPROCESS_BPSK_B1ISIM_HPP_

#include "../util/dataSource.hpp"
#include "../util/satInfo.hpp"

// ---------------
//  SIGNAL PARAMS
// ---------------

#define B1I_CARR_FREQ         1561.098e6
#define B1I_RANGING_CODE_RATE 2.046e6
#define B1I_DATA_RATE         50
#define B1I_NH_RATE           1000

// -------------------
//  SIMULATION PARAMS
// -------------------

#define MAX_CHANNEL_NUM 4

#endif