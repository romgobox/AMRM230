#! /usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime

from CRC16 import CRC16

def chSim(sim):
    sim = sim
    if len(sim)==1: sim = "0" + sim
    return sim
    
def udate():
    return datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")


def chCRC(cmd, CRC=CRC16(True)):
        if CRC.calculate(cmd[:-2]) == cmd[-2:]:
            return True
        else:
            return False
        

print chCRC('\x17\x00\x0E\x40')