/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:15
 * @LastEditTime: 2023-02-16 15:29:43
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

b1ISatInfo::b1ISatInfo(const json& raw_data, const int id) {
    this->data  = raw_data[id]["data"];
    this->prn   = raw_data[id]["prn"];
    this->delay = raw_data[id]["delay"];
    switch ((int)raw_data[id]["type"]) {
    case 1: this->type = GEO; break;
    case 2: this->type = IGSO; break;
    case 3: this->type = MEO; break;
    default: throw std::invalid_argument("satType error");
    }
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

b1IFileSource::b1IFileSource(const std::string& filepath) {
    std::ifstream f(filepath);
    this->sat_sata = json::parse(f);
}

b1ISatInfo b1IFileSource::getSatInfo(const int idx) {
    return b1ISatInfo(this->sat_sata[idx], idx);
}

} // namespace signalProcess