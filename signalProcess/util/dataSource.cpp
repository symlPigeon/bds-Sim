/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 22:55:30
 * @LastEditTime: 2023-03-07 23:10:22
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.cpp
 */

#include "dataSource.hpp"

namespace signalProcess {

bDataSource::bDataSource(const std::string& data, const int bitwidth)
    : data(data),
      dataLength(static_cast<int>(bitwidth * data.length())),
      dataIdx(0) {
    for (auto& i : data) {
        for (int j = 0; j < bitwidth; j++) {
            // MSB
            binData.push_back((i >> (bitwidth - j - 1)) & 0x01);
        }
    }
}

std::vector<int> bDataSource::getData() const {
    return this->binData;
}

int bDataSource::getLength() const {
    return this->dataLength;
}

int bDataSource::getNextBit() {
    int val       = this->binData[this->dataIdx];
    this->dataIdx = (this->dataIdx + 1) % this->dataLength;
    return val;
}

fDataSource::fDataSource(const std::vector<double>& data)
    : data(data), dataLength(static_cast<int>(data.size())), dataIdx(0) {}

std::vector<double> fDataSource::getData() const {
    return this->data;
}

int fDataSource::getLength() const {
    return this->dataLength;
}

double fDataSource::getNextData() {
    double val    = this->data[this->dataIdx];
    this->dataIdx = (this->dataIdx + 1) % this->dataLength;
    return val;
}

} // namespace signalProcess