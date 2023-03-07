/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 12:19:03
 * @LastEditTime: 2023-03-07 16:09:36
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Data Source Impl
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.cpp
 */

#include "dataSource.hpp"
#include <vector>

namespace signalProcess {

dataSource::dataSource(const std::string&         raw_data,
                       const std::vector<double>& delay,
                       const std::vector<double>& refDelay,
                       const std::vector<double>& elevation,
                       const int                  bitwidth)
    : raw_data(raw_data),
      delay(delay),
      refDelay(refDelay),
      elevation(elevation),
      dataIdx(0),
      delayIdx(0),
      refDelayIdx(0),
      elevationIdx(0) {
    for (auto& c : raw_data) {
        // convert c to int
        auto tmp = c - '0';
        // from MSB to LSB
        for (int i = bitwidth - 1; i >= 0; i--) {
            data.push_back((tmp >> i) & 0x1);
        }
    }
}

int dataSource::getData(int idx) const {
    return data[idx];
}

double dataSource::getDelay(bool update) {
    double val = delay[delayIdx];
    if (update) {
        delayIdx++;
        if (delayIdx >= delay.size()) {
            delayIdx = 0;
        }
    }
    return val;
}

double dataSource::getRefDelay(bool update) {
    double val = refDelay[refDelayIdx];
    if (update) {
        refDelayIdx++;
        if (refDelayIdx >= refDelay.size()) {
            refDelayIdx = 0;
        }
    }
    return val;
}

double dataSource::getElevation(bool update) {
    double val = elevation[elevationIdx];
    if (update) {
        elevationIdx++;
        if (elevationIdx >= elevation.size()) {
            elevationIdx = 0;
        }
    }
    return val;
}

int dataSource::getData(bool update) {
    int val = data[dataIdx];
    if (update) {
        dataIdx++;
        if (dataIdx >= data.size()) {
            dataIdx = 0;
        }
    }
    return val;
}

} // namespace signalProcess