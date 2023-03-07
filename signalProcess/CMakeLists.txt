cmake_minimum_required(VERSION 3.8)
project(BDS_SIM_TX)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")

set(UTIL_SRC util/satInfo.cpp util/dataSource.cpp)
set(UTIL_HEADER util/satInfo.hpp util/constants.hpp util/dataSource.hpp)

set(BPSK_SRC bpsk/b1isim.cpp)
set(BPSK_HEADER bpsk/b1isim.hpp)

add_executable(bpsk_sim ${UTIL_SRC} ${UTIL_HEADER} ${BPSK_SRC} ${BPSK_HEADER})