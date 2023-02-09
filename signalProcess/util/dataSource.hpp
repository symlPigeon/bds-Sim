/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-07 11:37:52
 * @LastEditTime: 2023-02-09 16:15:09
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Definition for dataSource
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.hpp
 */

#ifndef SIGNALPROCESS_UTIL_DATASOURCE_HPP_
#define SIGNALPROCESS_UTIL_DATASOURCE_HPP_

#include <gnuradio/sync_block.h>
#include <gnuradio/attributes.h>
#include <memory>
#include <vector>

namespace signalProcess {
class dataSource : virtual public gr::sync_block {
public:
    typedef std::shared_ptr<dataSource> sptr;
    static sptr                         make(const std::string& data,
                                             const int          bits_per_symbol,
                                             const bool         is_repeat,
                                             const int          init_phase);
};

class hexDataSource : public dataSource {
public:
    typedef std::shared_ptr<hexDataSource> sptr;
    static sptr
    make(const std::string& data, const bool is_repeat, const int init_phase);
};

class octDataSource : public dataSource {
public:
    typedef std::shared_ptr<octDataSource> sptr;
    static sptr
    make(const std::string& data, const bool is_repeat, const int init_phase);
};

class dataSource_impl : public dataSource {
private:
    std::vector<float> data;
    const int          bits_per_symbol;
    const bool         is_repeat;
    unsigned int       idx;
    const unsigned int data_size;

public:
    dataSource_impl(const std::string& data,
                    const int          bits_per_symbol,
                    const bool         is_repeat,
                    const int          init_phase);
    ~dataSource_impl(){};

    int work(int                        noutput_items,
             gr_vector_const_void_star& input_items,
             gr_vector_void_star&       output_items);
};

class hexDataSource_impl : public dataSource_impl, public hexDataSource {
public:
    hexDataSource_impl(const std::string& data,
                       const bool         is_repeat,
                       const int          init_phase = 0);
};

class octDataSource_impl : public dataSource_impl, public octDataSource {
public:
    octDataSource_impl(const std::string& data,
                       const bool         is_repeat,
                       const int          init_phase = 0);
};

} // namespace signalProcess

#endif