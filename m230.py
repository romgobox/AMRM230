#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from m230_class import m230
from dev_channel import DirectChannel as DC
from dev_channel import GSMChannel as GSM



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
    
    PPLR = merc.whPPValue(wh_adr_set, '49', '30')
    if PPLR:
        print 'Last Record Status: %s, Period: %s, A: %s, R: %s, DateTime: %s-%s-%s %s:%s' % \
        (PPLR['Status'], PPLR['Period'], PPLR['A'], PPLR['R'], PPLR['d'], PPLR['m'], PPLR['y'], PPLR['H'], PPLR['M'])
    else:
        print '!!!!'
    
    """
    print '--------------- U -------------'
    U = merc.whU(wh_adr_set)
    print "U1: " + str(U[1]) + " U2: " + str(U[2]) + " U3: " + str(U[3])
    
    print '--------------- I -------------'
    I = merc.whI(wh_adr_set)
    print "I1: " + str(I[1]) + " I2: " + str(I[2]) + " I3: " + str(I[3])
    """
    """
    MPDV = merc.whMPDVal(wh_adr_set, 48)
    
    for i in MPDV.values():
        print '-----------------------------------------------------------------------'
        print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
    """
    #test = merc.whTestCMD(useAdr = True, whAdr = wh_adr_set, Prefix='\x06\x83', HiB='ff', LoB='80', Postfix='\xD2')
    #test = merc.whMPDValFast(wh_adr_set, 20)
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
    
