cmake_minimum_required(VERSION 3.8)
project(BDS_SIM_TX)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")

find_package(Gnuradio "3.10" COMPONENTS
    blocks
    fec
    fft
    filter
    analog
    digital
    dtv
    audio
    channels
    pdu
    qtgui
    trellis
    uhd
    uhd UHD 4.0 RFNoC
    vocoder
    wavelet
    zeromq
    network
    soapy
)

find_package(nlohmann_json REQUIRED)
find_package(Boost COMPONENTS program_options REQUIRED)

set(CMAKE_AUTOMOC ON)

set(SOURCES_BPSK util/dataSource.cpp bpsk/bpsk_main.cpp util/satInfo.cpp bpsk/main.cpp)
set(SOURCES_BOC util/dataSource.cpp util/satInfo.cpp)

set(HEADERS_BPSK util/dataSource.hpp util/satInfo.hpp bpsk/bpsk_main.hpp)
set(HEADERS_BOC util/dataSource.hpp)

add_executable(bds_bpsk ${SOURCES_BPSK} ${HEADERS_BPSK})

target_link_libraries(bds_bpsk
    gnuradio::gnuradio-blocks
    nlohmann_json
    gnuradio-uhd uhd
    ${Boost_LIBRARIES}
)