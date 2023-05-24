/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:15
 * @LastEditTime: 2023-05-17 13:06:29
 * @LastEditors: symlpigeon
 * @Description: 用于存储卫星信息、解析bdsTx模块传输的数据  
 * @FilePath: \bds-Sim\signalProcess\util\satInfo.cpp
 */

#include "satInfo.hpp"
#include <exception>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <iostream>

using json = nlohmann::json;

namespace signalProcess {

b1ISatInfo::b1ISatInfo(const json& raw_data) {
    this->data  = raw_data["data"];
    this->prn   = raw_data["prn"];
    this->delay = std::vector<double>();
    for (auto& i : raw_data["delay"]) { this->delay.push_back(i); }
    this->refDelay = raw_data["refDelay"];
    this->elevation = std::vector<double>();
    for (auto& i : raw_data["elevation"]) { this->elevation.push_back(i); }
    switch ((int)raw_data["type"]) {
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

double b1ISatInfo::getRefDelay() const {
    return this->refDelay;
}

std::vector<double> b1ISatInfo::getElevation() const {
    return this->elevation;
}

b1IFileSource::b1IFileSource(const std::string& filepath) {
    std::ifstream f(filepath);
    this->sat_data = json::parse(f);
}

b1ISatInfo b1IFileSource::getSatInfo(const int idx) {
    return b1ISatInfo(this->sat_data[idx]);
}

unsigned int b1IFileSource::getSatCnt() const {
    return this->sat_data.size();
}

b1CSatInfo::b1CSatInfo(const json& raw_data) {
    this->data = raw_data["data"];
    this->iprn = raw_data["prn"];
    this->qprn = raw_data["qprn"];
    this->sub_qprn = raw_data["qprn_sub"];
    this->delay = std::vector<double>();
    for (auto& i : raw_data["delay"]) { this->delay.push_back(i); }
    this->refDelay = raw_data["refDelay"];
    this->elevation = std::vector<double>();
    for (auto& i : raw_data["elevation"]) { this->elevation.push_back(i); }
    switch ((int)raw_data["type"]) {
    case 1: this->type = GEO; break;
    case 2: this->type = IGSO; break;
    case 3: this->type = MEO; break;
    default: throw std::invalid_argument("satType error");
    }
}

std::string b1CSatInfo::getPrn() const {
    return this->iprn;
}

std::string b1CSatInfo::getData() const {
    return this->data;
}

satType b1CSatInfo::getType() const {
    return this->type;
}

std::vector<double> b1CSatInfo::getDelay() const {
    return this->delay;
}

double b1CSatInfo::getRefDelay() const {
    return this->refDelay;
}

std::vector<double> b1CSatInfo::getElevation() const {
    return this->elevation;
}

std::string b1CSatInfo::getQPrn() const {
    return this->qprn;
}

std::string b1CSatInfo::getSubQPrn() const {
    return this->sub_qprn;
}

b1CFileSource::b1CFileSource(const std::string& filepath) {
    std::ifstream f(filepath);
    this->sat_data = json::parse(f);
}

b1CSatInfo b1CFileSource::getSatInfo(const int idx) {
    return b1CSatInfo(this->sat_data[idx]);
}

unsigned int b1CFileSource::getSatCnt() const {
    return this->sat_data.size();
}

} // namespace signalProcess