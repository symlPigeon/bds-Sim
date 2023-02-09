/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:15
 * @LastEditTime: 2023-02-09 16:21:03
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 用于存储卫星信息、解析bdsTx模块传输的数据  
 * @FilePath: /bds-Sim/signalProcess/util/satInfo.cpp
 */

#include "satInfo.hpp"
#include <exception>
#include <fstream>
#include <stdexcept>
using json = nlohmann::json;

namespace signalProcess {
void b1ISatInfo::parseData() {
    std::ifstream f(this->filepath);
    json          raw_data = json::parse(f);
    this->data             = raw_data["data"];
    this->prn              = raw_data["prn"];
    this->delay            = raw_data["delay"];
    switch ((int)raw_data["type"]) {
    case 1: this->type = GEO; break;
    case 2: this->type = IGSO; break;
    case 3: this->type = MEO; break;
    default: throw std::invalid_argument("satType error");
    }
}

b1ISatInfo::b1ISatInfo(const std::string& filepath) : filepath(filepath) {
    this->parseData();
}

std::string b1ISatInfo::getPrn() const {
    return this->prn;
}

std::string b1ISatInfo::getData() const {
    return this->data;
}

satType b1ISatInfo::getType() const {
    return this->type;
}

int b1ISatInfo::getDelay() const {
    return this->delay;
}

} // namespace signalProcess