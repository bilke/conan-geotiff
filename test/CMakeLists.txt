project(MyTiff C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

include_directories(${GEOTIFF_INCLUDE_DIRS})
add_executable(geotifftest geotifftest.c)

target_link_libraries(geotifftest ${CONAN_LIBS})

if(UNIX AND NOT APPLE)
    TARGET_LINK_LIBRARIES(geotifftest m)
endif()
