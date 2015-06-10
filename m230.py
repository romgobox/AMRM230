#! /usr/bin/python
# -*- coding: utf-8 -*-

from m230_class import m230
from dev_channel import DirectChannel as DC



wh_adr_set = 145
wh_adr_set1 = 43
channel = DC('/dev/ttyUSB0', whTimeout=0.1)
merc = m230(channel)



merc.whAuth(wh_adr_set, 111111, 1)
print merc.whNum(wh_adr_set)
print merc.whTime(wh_adr_set)['DateTime']
m = merc.whMPDVal(wh_adr_set, 10)


for i in m.values():
    print '-----------------------------------------------------------------------'
    print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
    
print len(m)

merc.whLogOut(wh_adr_set)
