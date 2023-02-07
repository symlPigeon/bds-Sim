/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-07 11:38:03
 * @LastEditTime: 2023-02-07 12:42:00
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Implementation for dataSource
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.cpp
 */

#include "dataSource.hpp"

#include <gnuradio/io_signature.h>

namespace signalProcess {

dataSource_impl::dataSource_impl(const std::string& data,
                                 const int          bits_per_symbol,
                                 const bool         is_repeat)
    : gr::sync_block("dataSource",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, sizeof(float))),
      bits_per_symbol(bits_per_symbol),
      is_repeat(is_repeat),
      idx(0),
      data_size(data.size() * bits_per_symbol) {
    for (auto& c : data) {
        for (auto i = 0; i < bits_per_symbol; i++) {
            if (c & (1 << i)) {
                // 0 means 1
                this->data.push_back(-1);
            } else {
                // 1 means -1
                this->data.push_back(1);
            }
        }
    }
}

hexDataSource_impl::hexDataSource_impl(const std::string& data,
                                       const bool         is_repeat)
    : dataSource_impl(data, 4, is_repeat) {}

octDataSource_impl::octDataSource_impl(const std::string& data,
                                       const bool         is_repeat)
    : dataSource_impl(data, 3, is_repeat) {}

int dataSource_impl::work(int                        noutput_items,
                          gr_vector_const_void_star& input_items,
                          gr_vector_void_star&       output_items) {
    auto out = static_cast<float*>(output_items[0]);
    for (auto i = 0; i < noutput_items; i++) {
        out[i] = data[idx];
        idx = (idx + 1) % data_size;
    }
    return noutput_items;
}

} // namespace signalProcess