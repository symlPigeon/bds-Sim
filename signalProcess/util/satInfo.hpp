/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 12:59:01
 * @LastEditTime: 2023-02-09 16:20:54
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 用于存储卫星信息、解析bdsTx模块传输的数据
 * @FilePath: /bds-Sim/signalProcess/util/satInfo.hpp
 */

#ifndef SIGNALPROCESS_UTIL_SATINFO_HPP_
#define SIGNALPROCESS_UTIL_SATINFO_HPP_

#include <string>
#include <nlohmann/json.hpp>
#include <fstream>

namespace signalProcess {

enum satType { GEO, MEO, IGSO };

class b1ISatInfo {
private:
    std::string       data;
    std::string       prn;
    satType           type;
    int               delay;
    const std::string filepath;
    void              parseData();

public:
    b1ISatInfo(const std::string& filepath);
    ~b1ISatInfo(){};
    std::string getPrn() const;
    satType     getType() const;
    std::string getData() const;
    int         getDelay() const;
};

} // namespace signalProcess

#endif