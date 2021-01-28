cmake_minimum_required(VERSION 3.18.5)
project (main CXX)

find_package (Python3 COMPONENTS Interpreter)
set(PYTHON_VENV "${PROJECT_SOURCE_DIR}/.python_venv")
execute_process (COMMAND "${Python3_EXECUTABLE}" -m venv "${PYTHON_VENV}")

set(ENV{VIRTUAL_ENV} "${PYTHON_VENV}")
set(Python3_FIND_VIRTUALENV FIRST)
unset(Python3_EXECUTABLE)
find_package(Python3 COMPONENTS Interpreter)
set(CMAKE_PROGRAM_PATH "${PYTHON_VENV}/Scripts")

file(WRITE "${PYTHON_VENV}/requirements.txt" "conan\n")
execute_process(COMMAND "${Python3_EXECUTABLE}" -m pip install --upgrade pip)
execute_process(COMMAND "${Python3_EXECUTABLE}" -m pip install -r "${PYTHON_VENV}/requirements.txt" INPUT_FILE "${PYTHON_VENV}/requirements.txt")

# Download automatically, you can also just copy the conan.cmake file
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
   message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
   file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake" "${CMAKE_BINARY_DIR}/conan.cmake")
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)

conan_cmake_run(
    REQUIRES spdlog/1.8.2
    BASIC_SETUP
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(main main.cpp "CrabCups.h")
target_link_libraries(main ${CONAN_LIBS})
