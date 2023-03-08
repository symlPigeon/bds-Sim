/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-03-08 13:54:01
 * @LastEditTime: 2023-03-08 21:42:48
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: B1I Main
 * @FilePath: /bds-Sim/signalProcess/bpsk/b1imain.cpp
 */

#include "b1isim.hpp"
#include <cstddef>
#include <cstdlib>
#include <iostream>

using namespace signalProcess;

int main() {
    // read json file
    std::string   filepath = "./msg.json";
    b1IFileSource fileSource(filepath);

    // unsigned int channel_cnt = fileSource.getSatCnt();
    unsigned int channel_cnt = MAX_CHANNEL_NUM;

    // init channels
    b1iChannel channels[channel_cnt];
    for (int i = 0; i < channel_cnt; i++) {
        b1ISatInfo satInfo = fileSource.getSatInfo(i);
        channels[i]        = b1iChannel(satInfo);
    }

    // open output file and malloc memory
    short* iq_buff = (short*)calloc(static_cast<long>(2 * ITER_LENGTH), 2);
    signed char* iq8_buff =
        (signed char*)calloc(static_cast<long>(2 * ITER_LENGTH), 1);
    FILE* fp = fopen("./b1i.bin", "wb");

    for (int i = 0; i < SIMULATION_TIME / SIM_UPDATE_STEP; i++) {
        // 0.1 second
        for (int j = 0; j < ITER_LENGTH; j++) {
            int i_acc = 0;
            int q_acc = 0;
            for (int k = 0; k < channel_cnt; k++) {
                auto [iData, qData] = channels[k].getNextData();
                i_acc += iData;
                q_acc += qData;
            }

            i_acc = (i_acc + 64) >> 7;
            q_acc = (q_acc + 64) >> 7;

            iq_buff[static_cast<ptrdiff_t>(2 * j)]     = (short)i_acc;
            iq_buff[static_cast<ptrdiff_t>(2 * j + 1)] = (short)q_acc;
        }
        // fwrite(
        //     iq_buff, sizeof(short), static_cast<size_t>(2 * ITER_LENGTH), fp);
        for (int j = 0; j < 2 * ITER_LENGTH; j++) {
            iq8_buff[j] = (signed char)(iq_buff[j] >> 4);
        }
        fwrite(iq8_buff,
               sizeof(signed char),
               static_cast<size_t>(2 * ITER_LENGTH),
               fp);
        printf("Sencond %f Done!\n", i * 0.1);
    }
    std::cout << "Done!" << std::endl;
    free(iq_buff);
    fclose(fp);
    return 0;
}