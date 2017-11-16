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

import sys, signal
import numpy, zmq
import pmt


def string_to_hex(data):
    ''' Utility to convert a binary string to a hex string representation '''
    hex_string = ""
    for byte in numpy.fromstring(data, dtype=numpy.uint8):
        hex_string += hex(byte) + ' '
    return hex_string


def main():
    ''' Subscribe to a ZMQ port and print everything we see '''
    port = "14001"
    # port = "14000"  # Loopback testing
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print "Collecting ZMQ..."
    socket.connect("tcp://localhost:%s" % port)
    socket.setsockopt(zmq.SUBSCRIBE, '')  # Subscribe to everything

    while True:
        msg = socket.recv()
        pdu = pmt.deserialize_str(msg)
        car = pmt.to_python(pmt.car(pdu))
        cdr = pmt.to_python(pmt.cdr(pdu))
        cdr = numpy.getbuffer(cdr)  # flatten the vector bytes

        if car is not None:
            print car  # Print the dict
            # print '[car] Received [%i] bytes: %s' % (len(car), string_to_hex(car))
        if cdr is not None:
            print '[cdr] Received [%i] bytes: %s' % (len(cdr), string_to_hex(cdr))

def signal_handler(signal, frame):
    print("\nQuitting...")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()