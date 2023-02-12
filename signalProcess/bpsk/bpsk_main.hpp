/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-07 13:09:30
 * @LastEditTime: 2023-02-12 10:41:08
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: BPSK
 * @FilePath: /bds-Sim/signalProcess/bpsk/bpsk_main.hpp
 */

#ifndef SIGNALPROCESS_BPSK_BPSK_MAIN_HPP_
#define SIGNALPROCESS_BPSK_BPSK_MAIN_HPP_

#include <gnuradio/top_block.h>
#include <gnuradio/blocks/repeat.h>
#include <gnuradio/blocks/multiply.h>
#include <gnuradio/blocks/add_blk.h>
#include <gnuradio/blocks/float_to_complex.h>
#include <gnuradio/uhd/usrp_sink.h>

#include "../util/dataSource.hpp"
#include "../util/satInfo.hpp"

#define MAX_SAT_NUM 4

class bpsk_main {
private:
    //----------------//
    //   COMPONENTS   //
    //----------------//

    // 导航电文数据源
    signalProcess::octDataSource::sptr
        signalProcess_octDataSource_data[MAX_SAT_NUM];
    // NH码
    signalProcess::hexDataSource::sptr
        signalProcess_hexDataSource_nhcode[MAX_SAT_NUM];
    // 扩频码
    signalProcess::octDataSource::sptr
        signalProcess_octDataSource_spreadCode[MAX_SAT_NUM];
    // 导航电文到NH码，需要重复
    gr::blocks::repeat::sptr gr_blocks_repeat_dataToNHCode[MAX_SAT_NUM];
    // 经过NH码调制后，在扩频是也需要重复
    gr::blocks::repeat::sptr gr_blocks_repeat_dataToSpreadCode[MAX_SAT_NUM];
    // 扩频码增加到采样率
    gr::blocks::repeat::sptr gr_blocks_repeat_spreadCode[MAX_SAT_NUM];
    // NH码调制
    gr::blocks::multiply_ff::sptr gr_blocks_multiply_nhCode[MAX_SAT_NUM];
    // 扩频码调制
    gr::blocks::multiply_ff::sptr gr_blocks_multiply_spreadCode[MAX_SAT_NUM];
    // 合并信号
    gr::blocks::add_ff::sptr      gr_blocks_add_signal;
    // Float to Complex
    gr::blocks::float_to_complex::sptr gr_blocks_float_to_complex;
    // USRP Sink
    gr::uhd::usrp_sink::sptr      gr_uhd_usrp_sink;

    //----------------//
    //   CONSTANTS    //
    //----------------//

    // 信号带宽
    double              bandwidth = 2.046e6 * 2;
    // 采样率，信号带宽的两倍
    double              sample_rate = bandwidth * 2;
    // 数据速率
    double              d1_data_rate = 50;
    // float             d2_data_rate = 500; // NOTE: 暂不考虑GEO发布的D2电文
    // NH Code 速率
    double              nh_code_rate = 1000;
    // 测距码速率
    double              spread_code_rate = 2.046e6;
    // NH Code
    const std::string nh_code     = "04d4e"; // 00000100110101001110

    //----------------//
    //    RF PART     //
    //----------------//
    //
    // 信号频率
    double      signal_freq = 1561.098e6;
    std::string device      = "";
    double      gain        = 40;

public:
    //----------------//
    // REQUIRED DEFS  //
    //----------------//
    bpsk_main(const signalProcess::b1ISatInfo satInfo[MAX_SAT_NUM],
              const std::string&              uhd_addr);
    ~bpsk_main(){};
    gr::top_block_sptr tb;
    double             get_samp_rate() const;
    void               set_samp_rate(double samp_rate);
};

#endif
