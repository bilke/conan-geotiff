cmake_minimum_required(VERSION 2.8.12)
project(test_package)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories(${GEOTIFF_INCLUDE_DIRS})
add_executable(${PROJECT_NAME} test_package.c)

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})

if(UNIX AND NOT APPLE)
    TARGET_LINK_LIBRARIES(${PROJECT_NAME} m)
endif()
