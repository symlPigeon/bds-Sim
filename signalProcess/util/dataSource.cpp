/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-07 11:38:03
 * @LastEditTime: 2023-02-09 16:21:58
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Implementation for dataSource
 * @FilePath: /bds-Sim/signalProcess/util/dataSource.cpp
 */

#include "dataSource.hpp"

#include <gnuradio/io_signature.h>
#include <gnuradio/sptr_magic.h>

namespace signalProcess {

dataSource::sptr dataSource::make(const std::string& data,
                                  const int          bits_per_symbol,
                                  const bool         is_repeat,
                                  const int          init_phase) {
    return gnuradio::make_block_sptr<dataSource_impl>(
        data, bits_per_symbol, is_repeat, init_phase);
}

hexDataSource::sptr hexDataSource::make(const std::string& data,
                                        const bool         is_repeat,
                                        const int          init_phase) {
    return gnuradio::make_block_sptr<hexDataSource_impl>(
        data, is_repeat, init_phase);
}

octDataSource::sptr octDataSource::make(const std::string& data,
                                        const bool         is_repeat,
                                        const int          init_phase) {
    return gnuradio::make_block_sptr<octDataSource_impl>(
        data, is_repeat, init_phase);
}

dataSource_impl::dataSource_impl(const std::string& data,
                                 const int          bits_per_symbol,
                                 const bool         is_repeat,
                                 const int          init_phase)
    : gr::sync_block("dataSource",
                     gr::io_signature::make(0, 0, 0),
                     gr::io_signature::make(1, 1, sizeof(float))),
      bits_per_symbol(bits_per_symbol),
      is_repeat(is_repeat),
      idx(init_phase >= 0 ? init_phase
                          : data.length() * bits_per_symbol + init_phase),
      data_size(data.size() * bits_per_symbol) {
    // convert data to lower case
    std::string data_lower;
    for (auto& c : data) { data_lower.push_back(std::tolower(c)); }
    for (auto& c : data_lower) {
        // convert to decimal
        if (c >= '0' && c <= '9') {
            c -= '0';
        } else if (c >= 'a' && c <= 'f') {
            c -= 'a' - 10;
        } else {
            throw std::invalid_argument("Invalid data");
        }
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
                                       const bool         is_repeat,
                                       const int          init_phase)
    : dataSource_impl(data, 4, is_repeat, init_phase) {}

octDataSource_impl::octDataSource_impl(const std::string& data,
                                       const bool         is_repeat,
                                       const int          init_phase)
    : dataSource_impl(data, 3, is_repeat, init_phase) {}

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