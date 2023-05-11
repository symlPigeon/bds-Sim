cmake_minimum_required(VERSION 3.8)
project(BDS_SIM_TX)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb -static-libstdc++")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall -static-libstdc++")

set(UTIL_SRC util/satInfo.cpp util/dataSource.cpp)
set(UTIL_HEADER util/satInfo.hpp util/constants.hpp util/dataSource.hpp)

set(BPSK_SRC bpsk/b1isim.cpp bpsk/b1imain.cpp)
set(BPSK_HEADER bpsk/b1isim.hpp)

include(FetchContent)

FetchContent_Declare(json
  GIT_REPOSITORY https://github.com/ArthurSonzogni/nlohmann_json_cmake_fetchcontent
  GIT_PROGRESS TRUE
  GIT_SHALLOW TRUE
  GIT_TAG v3.11.2)
FetchContent_MakeAvailable(json)

add_executable(bpsk_sim ${UTIL_SRC} ${UTIL_HEADER} ${BPSK_SRC} ${BPSK_HEADER})
target_link_libraries(bpsk_sim PRIVATE nlohmann_json::nlohmann_json)