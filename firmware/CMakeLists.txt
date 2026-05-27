cmake_minimum_required(VERSION 3.16)

file(READ "${CMAKE_CURRENT_LIST_DIR}/../VERSION" PROJECT_VER_RAW)
string(STRIP "${PROJECT_VER_RAW}" PROJECT_VER)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(esp32_agent_firmware)
