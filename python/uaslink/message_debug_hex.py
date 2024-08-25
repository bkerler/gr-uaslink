#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Rearden Logic, Inc.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy, pmt
from gnuradio import gr

class message_debug_hex(gr.sync_block):
    """
    Message debugging output in hex
    """

    def __init__(self, description):
        gr.sync_block.__init__(self,
                               name="debug_print",
                               in_sig=None,
                               out_sig=None)
        self.message_port_register_in(pmt.intern("Control_IN"))
        self.set_msg_handler(pmt.intern("Control_IN"), self.control_handler)
        self.description = description  # know what's outputting

    def string_to_hex(self, data):
        ''' Utility to convert a binary string to a hex string representation '''
        hex_string = ""
        for byte in numpy.fromstring(data, dtype=numpy.uint8):
            hex_string += hex(byte)
            hex_string += ' '
        return hex_string

    def control_handler(self, msg):
        car = pmt.to_python(pmt.car(msg))
        cdr = pmt.to_python(pmt.cdr(msg))

        print ("=== Debugging %s ===" % (self.description))

        try:
            len_car = len(car)
        except:
            len_car = 0
        if len_car == 0:
            str_car = " "
        else:
            str_car = self.string_to_hex(car)

        try:
            len_cdr = len(cdr)
        except:
            len_cdr = 0
        if len_cdr == 0:
            str_cdr = " "
        else:
            str_cdr = self.string_to_hex(cdr)

        print ("[car %i bytes]: \n\t[string]:%s\n\t[hex]:%s" % (len_car, car, str_car))
        print ()
        print ("[cdr %i bytes]: \n\t[string]:%s\n\t[hex]%s:" % (len_cdr, cdr, str_cdr))

        print ("=== /Debugging %s ===" % (self.description))

    def work(self, input_items, output_items):
        pass
