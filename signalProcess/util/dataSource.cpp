/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 22:55:30
 * @LastEditTime: 2023-03-08 21:54:18
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.cpp
 */

#include "dataSource.hpp"
#include <cmath>

namespace signalProcess {

bDataSource::bDataSource(const std::string& data, const int bitwidth)
    : data(data),
      dataLength(static_cast<int>(bitwidth * data.length())),
      dataIdx(0) {
    for (auto& i : data) {
        for (int j = 0; j < bitwidth; j++) {
            // MSB
            binData.push_back(
                std::stoi(std::string() + i, 0, (int)std::pow(2, bitwidth))
                    >> (bitwidth - j - 1)
                & 0x01);
        }
    }
}

int bDataSource::getLength() const {
    return this->dataLength;
}

int bDataSource::getBit() {
    return this->binData[this->dataIdx];
}

int bDataSource::getBitAtIdx(const int idx) const {
    return this->binData[idx];
}

void bDataSource::next() {
    this->dataIdx++;
    if (this->dataIdx >= this->dataLength) {
        this->dataIdx = 0;
    }
}

void bDataSource::setIdx(const int idx) {
    this->dataIdx = idx % this->dataLength;
}

fDataSource::fDataSource(const std::vector<double>& data)
    : data(data), dataLength(static_cast<int>(data.size())), dataIdx(0) {}

int fDataSource::getLength() const {
    return this->dataLength;
}

double fDataSource::getData() {
    return this->data[this->dataIdx];
}

double fDataSource::getDataAtIdx(const int idx) const {
    return this->data[idx];
}

void fDataSource::next() {
    this->dataIdx++;
    if (this->dataIdx >= this->dataLength) {
        this->dataIdx = 0;
    }
}

void fDataSource::setIdx(const int idx) {
    this->dataIdx = idx % this->dataLength;
}

} // namespace signalProcess