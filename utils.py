#! /usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime

from CRC16 import CRC16 as CRCM230

def chSim(sim):
    sim = sim
    if len(sim)==1: sim = "0" + sim
    return sim
    
def udate():
    return datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")

"""
def chCRCM230(cmd, CRC=CRC16(True)):
        if CRC.calculate(cmd[:-2]) == cmd[-2:]:
            return True
        else:
            return False
"""
        

class CheckCRC(object):
    def __init__(self, cmd, whType=0):
        self.cmd = cmd
        self.whType = whType
        self.whTypeCRC = {
            0:CRCM230(True),
        }
        self.CRC = self.whTypeCRC[self.whType]
    
    def chCRCM230(self):
        if self.CRC.calculate(self.cmd[:-2]) == self.cmd[-2:]:
            return True
        else:
            return False
    #code

        
