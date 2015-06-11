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
 
