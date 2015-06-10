#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import serial


"""
class DevChannel():
    
    def __init__(self, ):
        pass
    
    def direct_channel(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(), whTimeout = 0.1):
    
        ser.port = port
        ser.baudrate = baudrate
        ser.bytesize = bytesize
        ser.parity = parity
        ser.stopbits = stopbits
        ser.timeout = timeout
        ser.writeTimeout = writeTimeout
        whTimeout = whTimeout
    
        try:
            ser.open()
        except Exception:
            print 'Port not found: ' + port
        else:
            print 'Port opened'
"""
    
class DirectChannel(object):
    
    def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(), whTimeout = 0.1):
        """
        Открывает прямой канал (как правило по протоколу RS-485) до счетчика.
        """
        self.ser = ser
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.timeout = timeout
        self.ser.writeTimeout = writeTimeout
        self.whTimeout = whTimeout
    
        try:
            self.ser.open()
        except Exception:
            print 'Port not found: ' + self.port
        else:
            print 'Port opened'
    
    def TX(self, cmd):
        self.ser.write(cmd)
    
    def RX(self):
       return self.ser.read(self.ser.inWaiting())
    


