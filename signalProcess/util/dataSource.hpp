/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 22:55:22
 * @LastEditTime: 2023-03-07 23:09:49
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: 
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.hpp
 */

#ifndef SIGNALPROCESS_UTIL_DATASOURCE_HPP_
#define SIGNALPROCESS_UTIL_DATASOURCE_HPP_

#include <string>
#include <vector>

namespace signalProcess {

/**
 * @brief A General data source
 * 
 */
class bDataSource {
private:
    std::string      data;
    std::vector<int> binData;
    int              dataLength;
    int              dataIdx;

public:
    bDataSource(const std::string& data, const int bitwidth);
    ~bDataSource(){};
    std::vector<int> getData() const;
    int              getLength() const;
    int              getNextBit();
};

class fDataSource {
private:
    std::vector<double> data;
    int                 dataLength;
    int                 dataIdx;

public:
    fDataSource(const std::vector<double>& data);
    ~fDataSource(){};
    std::vector<double> getData() const;
    int                 getLength() const;
    double              getNextData();
};

} // namespace signalProcess

#endif