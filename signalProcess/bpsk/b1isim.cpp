/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-26 10:54:48
 * @LastEditTime: 2023-03-07 16:20:05
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1I/B3I BPSK Simulation
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1isim.cpp
 */

#include "b1isim.hpp"
#include <cmath>

namespace signalProcess {

b1iChannel::b1iChannel(const signalProcess::b1ISatInfo& sat_info,
                       signalProcess::dataSource&       data_src)
    : sat_info(sat_info), data_src(data_src), carr_phase(0) {
    double r_ref      = data_src.getRefDelay(false);
    double r          = data_src.getDelay(false);
    double init_phase = (2 * r_ref - r) * B1I_CARR_FREQ;
    init_phase -= std::floor(init_phase);
    carr_phase = static_cast<unsigned int>(init_phase * 512 * 65536);
}
} // namespace signalProcess