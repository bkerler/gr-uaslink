# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT uaslink_sources)
    message(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT uaslink_sources)

########################################################################
# Check for pygccxml
########################################################################
gr_python_check_module_raw("pygccxml" "import pygccxml" PYGCCXML_FOUND)

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND uaslink_python_files python_bindings.cc)

gr_pybind_make_oot(uaslink ../../.. gr::uaslink "${uaslink_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(
    TARGET uaslink_python
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:uaslink_python>
            ${PROJECT_BINARY_DIR}/test_modules/gnuradio/uaslink/)

install(
    TARGETS uaslink_python
    DESTINATION ${GR_PYTHON_DIR}/gnuradio/uaslink
    COMPONENT pythonapi)
