##
##  Copyright (C) - Triton
##
##  This program is under the terms of the BSD License.
##

##################################################################################### CMake libtriton

cmake_minimum_required(VERSION 2.8)
project(triton)

# Define cmake options
option(PINTOOL "Build Triton with the Pin tool as tracer" OFF)
option(KERNEL4 "Pin will run on a Linux's kernel v4" ON)
option(PYTHON_BINDINGS "Enable Python bindings into the libtriton" ON)
option(STATICLIB "Build a static library" OFF)
option(INCBUILD "Increment the build number" OFF)


# Get architecture
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(ARCHITECTURE amd64)
else()
    set(ARCHITECTURE i386)
endif()

if(${TARGET} MATCHES "ia32")
    set(ARCHITECTURE i386)
endif()


# Triton version
if(INCBUILD)
    # Get and increment the build number
    file(READ ${CMAKE_SOURCE_DIR}/.build_number BUILD_NUMBER)
    math(EXPR NEW_BUILD_NUMBER "${BUILD_NUMBER} + 1")
    file(WRITE ${CMAKE_SOURCE_DIR}/.build_number ${NEW_BUILD_NUMBER})
endif()

file(READ ${CMAKE_SOURCE_DIR}/.build_number BUILD_NUMBER)
set(VERSION_MAJOR 0)
set(VERSION_MINOR 4)
set(VERSION_BUILD ${BUILD_NUMBER})

if(INCBUILD)
    # Update the PROJECT_NUMBER variable inside the Doxyfile
    file(READ ${CMAKE_SOURCE_DIR}/Doxyfile DOXYFILE)
    STRING(REGEX REPLACE "PROJECT_NUMBER[ ]*=[ ]*\"[a-zA-Z0-9. ]*\"" "PROJECT_NUMBER = \"version ${VERSION_MAJOR}.${VERSION_MINOR} build ${VERSION_BUILD}\"" PROJECT_NUMBER ${DOXYFILE})
    file(WRITE ${CMAKE_SOURCE_DIR}/Doxyfile ${PROJECT_NUMBER})
endif()


# Custom cmake search
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/CMakeModules/")



# Triton project
set(CMAKE_BUILD_TYPE Release)


# Specific OSX POLICY
if(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    if(POLICY CMP0025)
        cmake_policy(SET CMP0025 OLD) # report Apple's Clang as just Clang
    endif()
    if(POLICY CMP0042)
        cmake_policy(SET CMP0042 NEW) # MACOSX_RPATH
    endif()
endif()


# Find boost
find_package(Boost 1.55.0 REQUIRED)
include_directories("${Boost_INCLUDE_DIRS}")


# Find Python 2.7
if(PYTHON_BINDINGS)
  if(NOT PYTHON_INCLUDE_DIRS)
    set(PYTHON_INCLUDE_DIRS "$ENV{PYTHON_INCLUDE_DIRS}")
  endif()
  if(NOT STATICLIB) # Only if building dynamic library
    if(NOT PYTHON_LIBRARIES)
      set(PYTHON_LIBRARIES "$ENV{PYTHON_LIBRARIES}")
    endif()
    if(NOT PYTHON_INCLUDE_DIRS AND NOT PYTHON_LIBRARIES)
        find_package(PythonLibs 2.7 REQUIRED)
    endif()
  endif()
  include_directories(${PYTHON_INCLUDE_DIRS})
endif()


# Find Z3
if(NOT Z3_INCLUDE_DIRS)
  set(Z3_INCLUDE_DIRS "$ENV{Z3_INCLUDE_DIRS}")
endif()
if(NOT STATICLIB) # Only if building dynamic library
  if(NOT Z3_LIBRARIES)
    set(Z3_LIBRARIES "$ENV{Z3_LIBRARIES}")
  endif()
  if(NOT Z3_INCLUDE_DIRS AND NOT Z3_LIBRARIES)
      find_package(Z3 REQUIRED)
      if(NOT Z3_FOUND)
          message(FATAL_ERROR "Z3 not found")
      endif()
  endif()
endif()
include_directories(${Z3_INCLUDE_DIRS})


# Find Capstone
if(NOT CAPSTONE_INCLUDE_DIRS)
  set(CAPSTONE_INCLUDE_DIRS "$ENV{CAPSTONE_INCLUDE_DIRS}")
endif()
if(NOT STATICLIB) # Only if building dynamic library
  if(NOT CAPSTONE_LIBRARIES)
    set(CAPSTONE_LIBRARIES "$ENV{CAPSTONE_LIBRARIES}")
  endif()
  if(NOT CAPSTONE_INCLUDE_DIRS AND NOT CAPSTONE_LIBRARIES)
      find_package(CAPSTONE REQUIRED)
      if(NOT CAPSTONE_FOUND)
          message(FATAL_ERROR "Capstone not found")
      endif()
  endif()
endif()
include_directories(${CAPSTONE_INCLUDE_DIRS})

add_subdirectory(src)
