/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-07 12:53:16
 * @LastEditTime: 2023-02-09 16:57:02
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: BPSK
 * @FilePath: /bds-Sim/signalProcess/bpsk/bpsk_main.cpp
 */

// NOTE: 暂时不考虑GEO发布的D2电文

#include "bpsk_main.hpp"
#include <gnuradio/blocks/add_blk.h>
#include <gnuradio/blocks/multiply.h>
#include <gnuradio/blocks/repeat.h>
#include <gnuradio/uhd/usrp_sink.h>
#include <uhd/stream.hpp>

bpsk_main::bpsk_main(const signalProcess::b1ISatInfo satInfo[MAX_SAT_NUM]) {
    // Init the Top block
    this->tb = gr::make_top_block("BPSK-B1I/B3I");

    //---------------------------//
    //   INIT BLOCKs AND CONNs   //
    //---------------------------//

    this->gr_blocks_add_signal = gr::blocks::add_ff::make(4);

    for (auto i = 0; i < MAX_SAT_NUM; i++) {
        // NH码
        this->signalProcess_hexDataSource_nhcode[i] =
            signalProcess::hexDataSource_impl::hexDataSource::make(
                this->nh_code, true, 0);
        // FIXME: 搞清楚这两个延迟到底要怎么搞
        // 导航电文数据
        this->signalProcess_octDataSource_data[i] =
            signalProcess::octDataSource_impl::octDataSource::make(
                satInfo[i].getData(), true, satInfo[i].getDelay());
        // 扩频码
        this->signalProcess_octDataSource_spreadCode[i] =
            signalProcess::octDataSource_impl::octDataSource::make(
                satInfo[i].getPrn(), true, satInfo[i].getDelay());

        // NH码调制
        // 数据码字50bps, NH码字1kbps, 50/1000=1/20
        this->gr_blocks_repeat_dataToNHCode[i] = gr::blocks::repeat::make(
            sizeof(float), int(this->nh_code_rate / this->d1_data_rate));
        this->gr_blocks_multiply_nhCode[i] = gr::blocks::multiply_ff::make(2);
        this->tb->hier_block2::connect(
            this->signalProcess_octDataSource_data[i],
            0,
            this->gr_blocks_repeat_dataToNHCode[i],
            0);
        this->tb->hier_block2::connect(this->gr_blocks_repeat_dataToNHCode[i],
                                       0,
                                       this->gr_blocks_multiply_nhCode[i],
                                       0);
        this->tb->hier_block2::connect(
            this->signalProcess_hexDataSource_nhcode[i],
            0,
            this->gr_blocks_multiply_nhCode[i],
            1);

        // 扩频码调制
        // 扩频码速率20.46e6, NH调制后速率1e3
        this->gr_blocks_repeat_dataToSpreadCode[i] = gr::blocks::repeat::make(
            sizeof(float), int(this->sample_rate / this->nh_code_rate));
        this->gr_blocks_repeat_spreadCode[i] = gr::blocks::repeat::make(
            sizeof(float), int(this->sample_rate / this->spread_code_rate));
        this->gr_blocks_multiply_spreadCode[i] =
            gr::blocks::multiply_ff::make(2);
        this->tb->hier_block2::connect(
            this->gr_blocks_multiply_nhCode[i],
            0,
            this->gr_blocks_repeat_dataToSpreadCode[i],
            0);
        this->tb->hier_block2::connect(
            this->gr_blocks_repeat_dataToSpreadCode[i],
            0,
            this->gr_blocks_multiply_spreadCode[i],
            0);
        this->tb->hier_block2::connect(
            this->signalProcess_octDataSource_spreadCode[i],
            0,
            this->gr_blocks_repeat_spreadCode[i],
            0);
        this->tb->hier_block2::connect(this->gr_blocks_repeat_spreadCode[i],
                                       0,
                                       this->gr_blocks_multiply_spreadCode[i],
                                       1);

        // 累加数据
        this->tb->hier_block2::connect(this->gr_blocks_multiply_spreadCode[i],
                                       0,
                                       this->gr_blocks_add_signal,
                                       i);
    }
    // Convert to complex
    this->gr_blocks_float_to_complex = gr::blocks::float_to_complex::make(1);
    this->tb->hier_block2::connect(
        this->gr_blocks_add_signal, 0, this->gr_blocks_float_to_complex, 0);
    // USRP
    this->gr_uhd_usrp_sink =
        gr::uhd::usrp_sink::make(this->device, ::uhd::stream_args_t("fc32"));
    this->gr_uhd_usrp_sink->set_samp_rate(this->sample_rate);
    this->gr_uhd_usrp_sink->set_center_freq(this->center_freq);
    this->gr_uhd_usrp_sink->set_gain(this->gain);
    this->gr_uhd_usrp_sink->set_antenna("TX/RX", 0);
    this->gr_uhd_usrp_sink->set_time_unknown_pps(::uhd::time_spec_t());
    this->tb->hier_block2::connect(
        this->gr_blocks_float_to_complex, 0, this->gr_uhd_usrp_sink, 0);
}

// callbacks
double bpsk_main::get_samp_rate() const {
    return this->sample_rate;
}

void bpsk_main::set_samp_rate(double sample_rate) {
    this->sample_rate = sample_rate;
}