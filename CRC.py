#! /usr/bin/python
# -*- coding: utf-8 -*-

from ctypes import c_ushort

class CRC_M230(object):
    crc16_tab = []

    # The CRC's are computed using polynomials. Here is the most used coefficient for CRC16
    crc16_constant = 0xA001 # 40961

    def __init__(self, modbus_flag = False):
        if not len(self.crc16_tab): self.init_crc16()         # initialize the precalculated tables
        self.mdflag = bool(modbus_flag)


    def calculate(self, string = ''):
        try:
            if not isinstance(string, str): raise Exception("Please provide a string as argument for calculation.")
            if not string: return 0

            crcValue = 0x0000 if not self.mdflag else 0xffff

            for c in string:
                tmp = crcValue ^ ord(c)
                crcValue = (c_ushort(crcValue >> 8).value) ^ int(self.crc16_tab[(tmp & 0x00ff)], 0)
            CRC_bytes = self.lhBytes(crcValue)
            #CRC = [(hex(CRC_bytes[0]))[2:4], (hex(CRC_bytes[1]))[2:4]]
            #CRC = [CRC_bytes[0], CRC_bytes[1]]
            #return CRC
            CRC = chr(CRC_bytes[0]) + chr(CRC_bytes[1])
            return CRC
        except Exception, e:
            print "EXCEPTION(calculate): {}".format(e)
    
    def check(self, cmd):
        if self.calculate(cmd[:-2]) == cmd[-2:]:
            return True
        else:
            return False

    def lhBytes(self, data):
        return (data & 0xFF, ( data >> 8 ) & 0xFF)
    
    def init_crc16(self):
        '''The algorithm use tables with precalculated values'''
        for i in range(0, 256):
            crc = c_ushort(i).value
            for j in range(0, 8):
                if (crc & 0x0001):  crc = c_ushort(crc >> 1).value ^ self.crc16_constant
                else:               crc = c_ushort(crc >> 1).value
            self.crc16_tab.append(hex(crc))
