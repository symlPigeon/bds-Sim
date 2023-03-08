/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 22:55:22
 * @LastEditTime: 2023-03-08 16:04:50
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
    bDataSource(){};
    ~bDataSource(){};
    int              getLength() const;
    int              getBitAtIdx(const int idx) const;
    int              getBit();
    void             next();
    void             setIdx(const int idx);
};

class fDataSource {
private:
    std::vector<double> data;
    int                 dataLength;
    int                 dataIdx;

public:
    fDataSource(const std::vector<double>& data);
    fDataSource(){};
    ~fDataSource(){};
    int                 getLength() const;
    double              getDataAtIdx(const int idx) const;
    double              getData();
    void                next();
    void                setIdx(const int idx);
};

} // namespace signalProcess

#endif