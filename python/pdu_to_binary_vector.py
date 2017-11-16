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

class pdu_to_binary_vector(gr.sync_block):
    """
    Receive a PDU and create a PDU with a vector of bits
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="pdu_to_binary_vector",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern("Control_IN"))
        self.message_port_register_out(pmt.intern("Vector_OUT"))
        self.set_msg_handler(pmt.intern("Control_IN"), self.control_handler)

    def string_to_hex(self, data):
        ''' Utility to convert a binary string to a hex string representation '''
        hex_string = ""
        for byte in numpy.fromstring(data, dtype=numpy.uint8):
            hex_string += hex(byte) + ' '
        return hex_string


    def control_handler(self, msg):
        meta = pmt.car(msg)
        data = pmt.to_python(pmt.cdr(msg))

        print "\n=== zmq_to_pdu_vector ==="
        print '\tEncoding [%i] bytes: %s' % (len(data), self.string_to_hex(data))

        bufnp = numpy.unpackbits(numpy.fromstring(data, dtype=numpy.uint8))  # Convert to BPSK vectors of 0x00 or 0x01
        # print '\tSymbols: [%i] bits:\t%s' % (len(bufnp), bufnp)

        self.message_port_pub(pmt.intern("Vector_OUT"), pmt.cons(meta, pmt.to_pmt(bufnp)))


    def work(self, input_items, output_items):
        pass
