#!/usr/bin/env python

import zmq, pmt, time
from bitstring import *
import serial
import numpy
import threading
import signal
import sys
import time

def string_to_hex(data):
    ''' Utility to convert a binary string to a hex string representation '''
    hex_string = ""
    for byte in numpy.fromstring(data, dtype=numpy.uint8):
        hex_string += hex(byte) + ' '
    return hex_string


class ZMQ_Serial_Mavlink():
    def __init__(self,port="/dev/ttyACM0",baud=57600,
            zmq_sub_addr="tcp://127.0.0.1:14001",
            zmq_pub_addr="tcp://127.0.0.1:14000"):
        
        self.ser_port=port
        self.ser_baud=baud
        
        self.quit=False
        
        self.ctx = zmq.Context()
        
        self.zmq_meta=dict()
        
        #zmq tx
        self.tx_sock = self.ctx.socket(zmq.PUB)
        self.tx_sock.setsockopt(zmq.LINGER, 0)
        self.tx_sock.bind(zmq_pub_addr)
    
        #zmq_rx
        self.rx_sock = self.ctx.socket(zmq.SUB)
        self.rx_sock.setsockopt(zmq.LINGER, 0)
        self.rx_sock.connect(zmq_sub_addr)
        self.rx_sock.setsockopt(zmq.SUBSCRIBE, '')  # Subscribe to everything
    
    def start(self):
        #serial port
        self.ser = serial.Serial(self.ser_port, self.ser_baud, timeout=1)
        
        #launch threads
        self._t_ser = threading.Thread(target=self.serial_rx_thread_proc)
        self._t_ser.start()
        self._t_zmq = threading.Thread(target=self.zmq_rx_thread_proc)
        self._t_zmq.start()

        self._t_meta_relay = threading.Thread(target=self.meta_relay_thread_proc)
        self._t_zmq.start()
        
    def stop(self):
        self.quit=True
        self._t_ser.join()
        self._t_zmq.join()
        
        self.ser.close()
        
    def serial_rx_thread_proc(self):
        print "enter:serial_rx_thread_proc"
        
        with serial.Serial(self.ser_port, self.ser_baud, timeout=1) as ser:
            while not self.quit:
                if self.ser.inWaiting():
                    data=self.ser.read(500)
                    self.send_zmq(data)
                time.sleep(0.5)
                
        print "exit:serial_rx_thread_proc"
            
    def zmq_rx_thread_proc(self):
        print "enter:zmq_rx_thread_roc"
        
        poller = zmq.Poller()
        poller.register(self.rx_sock, zmq.POLLIN)
    
        while not self.quit:
            socks = dict(poller.poll(500))
            if self.rx_sock in socks and socks[self.rx_sock] == zmq.POLLIN:
                msg = self.rx_sock.recv()
            
                pdu = pmt.deserialize_str(msg)
                meta = pmt.to_python(pmt.car(pdu))
                data = pmt.to_python(pmt.cdr(pdu))
                data = numpy.getbuffer(data)  # flatten the vector bytes
                
                if car is not None:
                    print "zmq_rx:",meta  # Print the dict
                    # print '[car] Received [%i] bytes: %s' % (len(car), string_to_hex(car))
                    self.zmq_meta.update(meta)
                if data is not None:
                    #print 'zmq_rx:[cdr] Received [%i] bytes: %s' % (len(cdr), string_to_hex(cdr))r
                    print 'zmq_rx:[cdr] Received [%i] bytes' % (len(data))

                #self.ser.write(data.tobytes())
                self.ser.write(data)

        print "exit:zmq_rx_thread_proc"

    def meta_relay_thread_proc(self):
        """send some radio link meta data on the reverse link
        
        {'cfo': 100.9404296875, 'npkt_ok': 4, 'header_pass_rate': 100.0, 
        'es::event_length': 8192L, 'timestamp': 1510259309.3105321, 'est_len': 8299, 
        'orig_len': 8192, 'rx_rate': (0L, 199999.99937668347), 'es::event_type': 'edge_event',
        'es::event_time': 367994L, 'sync_delay': 8300, 'npkt_hok': 4, 
        'es::event_buffer': (array([  0,   0,   0, ...,   1,  16, 187], dtype=uint8), None),
        'payload_pass_rate': 100.0, 'rx_freq': (0L, 3017000000.0), 
        'rx_time': (0L, (1L, 0.60202746593035106)), 'npkt': 4}
        """
        while not self.quit:
            self.zmq_meta=dict()
            d=self.zmq_meta
            #bits = Bits(hex="13371337")
            #bits = Bits(int=int(d.get('header_pass_rate',0)), length=8)
            
            s="hpr:%.1f,ppr:%.1f,cfo:%.2f"%( d.get('header_pass_rate',0.0), 
                d.get('payload_pass_rate',0.0),d.get('cfo',0.0))
                
            car = pmt.make_dict()
            cdr = pmt.to_pmt(data)
            pdu = pmt.cons(car, cdr)

            # Status debug
            # print meta, type(meta), '\tmeta'
            # print pmtdata, type(pmtdata), '\tpmtdata'
            # print msg, type(msg), '\tmsg'

            #print 'send_zmq: Sending [%d] byte payload: %s' % (len(data), string_to_hex(data))
            self.tx_sock.send(pmt.serialize_str(pdu))

            time.sleep(1)
            
    def send_zmq(self, data):
        # Build the PDU
        car = pmt.make_dict()
        cdr = pmt.to_pmt(data)
        pdu = pmt.cons(car, cdr)

        # Status debug
        # print meta, type(meta), '\tmeta'
        # print pmtdata, type(pmtdata), '\tpmtdata'
        # print msg, type(msg), '\tmsg'

        #print 'send_zmq: Sending [%d] byte payload: %s' % (len(data), string_to_hex(data))
        self.tx_sock.send(pmt.serialize_str(pdu))

    
        
if __name__ == "__main__":
    zs=ZMQ_Serial_Mavlink()

    def signal_handler(signal, frame):
        print('Caught Ctrl+C!')
        zs.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    zs.start()
    
    while True:
        time.sleep(1)
        
