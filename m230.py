#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from m230_class import m230
from dev_channel import DirectChannel as DC
from dev_channel import GSMChannel as GSM


test
"""
wh_adr_set = 145
wh_adr_set1 = 43
channel = DC('/dev/ttyUSB0', whTimeout=2)
merc = m230(channel)
"""
wh_adr_set = 145
#channel = GSM('/dev/ttyUSB0', phone_number = '89659334537')
channel = DC(port = '/dev/ttyUSB0', whTimeout=2)


merc = m230(channel)

if merc.whAuth(wh_adr_set, 111111, 1):
    print 'WhNum: ' + merc.whNum(wh_adr_set)
    whTime = merc.whTime(wh_adr_set, datetimefrmt='%Y-%m-%d %H:%M:%S')
    

    print '--------------- U -------------'
    U = merc.whU(wh_adr_set)
    print repr(U)
    print 'U1: %s, U2: %s U3: %s' % (U[1],U[2],U[3],)
    
    A = merc.whUAngle(whAdr=145)
    print 'A12: %s, A13: %s A23: %s' % (A[12],A[13],A[23],)
    
    print '--------------- I -------------'
    I = merc.whI(wh_adr_set)
    print "I1: " + str(I[1]) + " I2: " + str(I[2]) + " I3: " + str(I[3])
    
    C = merc.whCosf(wh_adr_set)
    print 'C1: %.2f, C2: %.2f C3: %.2f' % (C[1],C[2],C[3],)
    print repr(C) 

    merc.whLogOut(wh_adr_set)
    
#channel.terminate()
"""
channel = GSM('/dev/ttyUSB0')
channel.GSMCall('89659334537')
time.sleep(10)
channel.GSMTerminate()
"""

"""
if merc.whAuth(wh_adr_set, 111111, 1):
    print merc.whNum(wh_adr_set)
    whTime = merc.whTime(wh_adr_set, datetimefrmt='%Y-%m-%d %H:%M:%S')
    print 'Wh: '+whTime['DateTime']
    print 'Sr: ' + str(datetime.datetime.now())
    whTD = whTime['TimeDiff']
    print whTD 
    m = merc.whMPDVal(wh_adr_set, 1)
"""
    
