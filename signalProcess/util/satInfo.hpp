/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:01
 * @LastEditTime: 2023-03-07 15:32:24
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 用于存储卫星信息、解析bdsTx模块传输的数据
 * @FilePath: /bds-Sim/signalProcess/util/satInfo.hpp
 */

#ifndef SIGNALPROCESS_UTIL_SATINFO_HPP_
#define SIGNALPROCESS_UTIL_SATINFO_HPP_

#include <string>
#include <nlohmann/json.hpp>
#include <fstream>

using json = nlohmann::json;

namespace signalProcess {

enum satType { GEO, MEO, IGSO };

class b1ISatInfo {
private:
    std::string         data;
    std::string         prn;
    satType             type;
    std::vector<double> delay;
    std::vector<double> refDealy;
    std::vector<double> elevation;

public:
    b1ISatInfo(const json& raw_data, const int id);
    ~b1ISatInfo(){};
    std::string         getPrn() const;
    satType             getType() const;
    std::string         getData() const;
    std::vector<double> getDelay() const;
    std::vector<double> getRefDelay() const;
    std::vector<double> getElevation() const;
};

class b1IFileSource {
private:
    json sat_sata;

public:
    b1IFileSource(const std::string& filepath);
    ~b1IFileSource(){};
    b1ISatInfo getSatInfo(const int idx);
};

} // namespace signalProcess

#endif