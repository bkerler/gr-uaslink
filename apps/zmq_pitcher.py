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

import zmq, pmt, time
from bitstring import *
import numpy


class Control:
    def __init__(self):
        pass

    def zmq_setup(self, zmq_addr):
        self.timeout = 100
        self.ctx = zmq.Context()
        self.zmqc = self.ctx.socket(zmq.PUB)
        self.zmqc.setsockopt(zmq.LINGER, 0)
        self.zmqc.bind(zmq_addr)

    def string_to_hex(self, data):
        ''' Utility to convert a binary string to a hex string representation '''
        hex_string = ""
        for byte in numpy.fromstring(data, dtype=numpy.uint8):
            hex_string += hex(byte)
            hex_string += ' '
        return hex_string

    def send_binary(self, data):
        # Build the PDU
        car = pmt.make_dict()
        cdr = pmt.to_pmt(data)
        pdu = pmt.cons(car, cdr)

        # Status debug
        # print meta, type(meta), '\tmeta'
        # print pmtdata, type(pmtdata), '\tpmtdata'
        # print msg, type(msg), '\tmsg'

        print 'Sending [%d] byte payload: %s' % (len(data), self.string_to_hex(data))
        self.zmqc.send(pmt.serialize_str(pdu))


def main():
    control = Control()
    control.zmq_setup('tcp://127.0.0.1:14000')
    time.sleep(.2)  # FixMe: This seems to be required or else we drop the first message, check for ready state -KDS

    data = BitArray('0xDEADBEEF')
    data = data * 10
    data = data.tobytes()  # Send a string of binary data uint8

    for i in xrange(1):
        print "----------------------"
        control.send_binary(data)
        time.sleep(.5)


if __name__ == "__main__":
    main()
