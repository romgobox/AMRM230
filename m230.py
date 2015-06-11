#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from m230_class import m230
from dev_channel import DirectChannel as DC


now = datetime.datetime.now()
delta = datetime.timedelta()

wh_adr_set = 145
wh_adr_set1 = 43
channel = DC('/dev/ttyUSB0', whTimeout=0.5)
merc = m230(channel)



merc.whAuth(wh_adr_set, 111111, 1)
print merc.whNum(wh_adr_set)
print merc.whTime(wh_adr_set)['DateTime']
m = merc.whMPDVal(wh_adr_set, 1)

print "************************************************************"
print merc.whTestCMD(useAdr=True, whAdr=wh_adr_set, Prefix='\x06\x83', HiB='00', LoB='00', Postfix='\xD2')
print merc.whTestCMD(useAdr=True, whAdr=wh_adr_set, Prefix='\x06\x83', HiB='00', LoB='E0', Postfix='\xD1')
print merc.whTestCMD(useAdr=True, whAdr=wh_adr_set, Prefix='\x06\x83', HiB='01', LoB='C0', Postfix='\xD2')
print "*****************************************"

print merc.whMPVal(whAdr=wh_adr_set, HiB='00', LoB='00')
print merc.whMPVal(whAdr=wh_adr_set, HiB='00', LoB='10')
print merc.whMPVal(whAdr=wh_adr_set, HiB='00', LoB='20')
print merc.whMPVal(whAdr=wh_adr_set, HiB='ff', LoB='f0')
#for i in m.values():
#    print '-----------------------------------------------------------------------'
#    print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
    
#print len(m)
"""
print "*****************  U  ************************************"
print u"Напряжение: "
print merc.whU(wh_adr_set)
print "************************************************************"
print "*****************  I  ************************************"
print u"Ток: "
print merc.whI(wh_adr_set)
print "************************************************************"

print "*****************  P  ************************************"
print u"Мощность: "
print merc.whP(wh_adr_set, 'S')
print "************************************************************"


print "*****************  Cosf  ************************************"
print u"Cosf: "
print merc.whCosf(wh_adr_set)
print "************************************************************"

print "*****************  Angle  ************************************"
print u"Углы между фазами: "
print merc.whUAngle(wh_adr_set)
print "************************************************************"
"""
merc.whLogOut(wh_adr_set)
