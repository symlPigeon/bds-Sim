/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-07 12:18:52
 * @LastEditTime: 2023-03-07 16:07:26
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Data Source
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.hpp
 */

#ifndef SIGNALPROCESS_UTIL_DATASOURCE_HPP_
#define SIGNALPROCESS_UTIL_DATASOURCE_HPP_

#include <string>
#include <vector>

namespace signalProcess {

/**
 * @brief Data Source
 * 
 */
class dataSource {
private:
    std::string         raw_data;
    std::vector<int>    data;
    std::vector<double> delay;
    std::vector<double> refDelay;
    std::vector<double> elevation;
    int                 dataIdx;
    int                 delayIdx;
    int                 refDelayIdx;
    int                 elevationIdx;

public:
    /**
    * @brief Construct a new dataSource object
    * 
    * @param raw_data 原始帧数据
    * @param delay 各个帧对应的延迟
    * @param refDelay 各个帧对应的参考延迟
    * @param bitwidth 原始帧数据的比特位宽，对于hex数据，bitwidth=4
    */
    dataSource(const std::string&         raw_data,
               const std::vector<double>& delay,
               const std::vector<double>& refDelay,
               const std::vector<double>& elevation,
               const int                  bitwidth);
    ~dataSource(){};

    /**
     * @brief Get the Data bit at idx
     * 
     * @param idx 
     * @return int 
     */
    int getData(const int idx) const;

    /**
     * @brief Get the Delay object
     * 
     * @param update 
     * @return double 
     */
    double getDelay(bool update = true);

    /**
     * @brief Get the reference delay of current frame
     * 
     * @param update
     * @return double 
     */
    double getRefDelay(bool update = true);

    /**
     * @brief Get the next data bit.
     * 
     * @param update 
     * @return int 
     */
    int getData(bool update = true);

    /**
     * @brief Get the elevation of current frame
     * 
     * @param update 
     * @return double 
     */
    double getElevation(bool update = true);
};

class hexDataSource : public dataSource {
public:
    hexDataSource(const std::string&         raw_data,
                  const std::vector<double>& delay,
                  const std::vector<double>& refDelay,
                  const std::vector<double>& elevation)
        : dataSource(raw_data, delay, refDelay, elevation, 4){};
    ~hexDataSource(){};
};

class octDataSource : public dataSource {
public:
    octDataSource(const std::string&         raw_data,
                  const std::vector<double>& delay,
                  const std::vector<double>& refDelay,
                  const std::vector<double>& elevation)
        : dataSource(raw_data, delay, refDelay, elevation, 3){};
    ~octDataSource(){};
};

} // namespace signalProcess

#endif