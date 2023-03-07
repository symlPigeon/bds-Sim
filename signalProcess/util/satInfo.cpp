/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:15
 * @LastEditTime: 2023-03-07 15:35:49
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
    this->delay = std::vector<double>();
    for (auto& i : raw_data[id]["delay"]) { this->delay.push_back(i); }
    this->refDealy = std::vector<double>();
    for (auto& i : raw_data[id]["refDelay"]) { this->refDealy.push_back(i); }
    this->elevation = std::vector<double>();
    for (auto& i : raw_data[id]["elevation"]) { this->elevation.push_back(i); }
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

std::vector<double> b1ISatInfo::getDelay() const {
    return this->delay;
}

std::vector<double> b1ISatInfo::getRefDelay() const {
    return this->refDealy;
}

std::vector<double> b1ISatInfo::getElevation() const {
    return this->elevation;
}

b1IFileSource::b1IFileSource(const std::string& filepath) {
    std::ifstream f(filepath);
    this->sat_sata = json::parse(f);
}

b1ISatInfo b1IFileSource::getSatInfo(const int idx) {
    return b1ISatInfo(this->sat_sata[idx], idx);
}

} // namespace signalProcess