/*
 * @Author: symlPigeon 2163953074@qq.com
 * @Date: 2023-02-09 14:43:45
 * @LastEditTime: 2023-02-12 10:38:34
 * @LastEditors: symlPigeon 2163953074@qq.com
 * @Description: Entry point for the application.
 * @FilePath: /bds-Sim/signalProcess/bpsk/main.cpp
 */

#include "bpsk_main.hpp"

#include <boost/program_options.hpp>
#include <cstddef>

namespace po = boost::program_options;

int main(int argc, char** argv) {
    // USRP PARAMS
    std::string             device = "";
    // Sat Params
    std::string             sat_filepath = "";
    po::options_description desc("Options");
    desc.add_options()("help", "display help")(
        "filepath", po::value<std::string>(&sat_filepath), "sat filepath")(
        "device", po::value<std::string>(&device), "device");
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("help")) {
        std::cout << desc << std::endl;
        return 0;
    }
    if (vm.count("filepath")) {
        std::cout << "Sat filepath: " << sat_filepath << std::endl;
    } else {
        std::cout << "Sat filepath not set" << std::endl;
        return 0;
    }
    signalProcess::b1IFileSource sat_source(sat_filepath);
    signalProcess::b1ISatInfo    sat_info[MAX_SAT_NUM] = {
        signalProcess::b1ISatInfo(sat_source.getSatInfo(0)),
        signalProcess::b1ISatInfo(sat_source.getSatInfo(1)),
        signalProcess::b1ISatInfo(sat_source.getSatInfo(2)),
        signalProcess::b1ISatInfo(sat_source.getSatInfo(3)),
    };

    bpsk_main* tx = new bpsk_main(sat_info, device);
    tx->tb->start();
    std::cin.ignore();
    tx->tb->stop();
    tx->tb->wait();
    return 0;
}