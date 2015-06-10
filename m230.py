#! /usr/bin/python
# -*- coding: utf-8 -*-
#check git ignoe
import m230_class

wh_adr_set = 145
wh_adr_set1 = 43
merc = m230_class.m230('/dev/ttyUSB0', whTimeout=0.1)

'''
#print merc.chCRC('\x90\x50\x90\x50\x12\x14\x03\x20\x05\x15\x01\x02\x4e')
#print merc.chCRC('\x90\x50\x12\x14\x03\x20\x05\x15\x01\x02\x4e')
if whCall(merc.ser, '89191504625'):
    try:
        
        merc.whAuth(wh_adr_set, 111111, 1)
        print merc.whNum(wh_adr_set)
        print merc.whTime(wh_adr_set)['DateTime']
        m = merc.whMPDVal(wh_adr_set, 10)
    
        for i in m.values():
            print '-----------------------------------------------------------------------'
            print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
        
        print len(m)
        
        merc.whAuth(wh_adr_set1, 111111, 1)
        print merc.whNum(wh_adr_set1)
        print merc.whTime(wh_adr_set1)['DateTime']
        n = merc.whMPDVal(wh_adr_set1, 10)
    
        for i in n.values():
            print '-----------------------------------------------------------------------'
            print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
        
        print len(m)
        
    except Exception:
        print "Cant establish connect with Wh. Stop GSM:"
        whCallTerm(merc.ser)

'''


merc.whAuth(wh_adr_set, 111111, 1)
print merc.whNum(wh_adr_set)
print merc.whTime(wh_adr_set)['DateTime']
m = merc.whMPDVal(wh_adr_set, 10)

for i in m.values():
    print '-----------------------------------------------------------------------'
    print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
    
print len(m)

print merc.chCRC('\x90\x05\xad\xb3')

#merc.whAuth(145, 111111, 1)
'''
n = merc.whNum(145)
t = merc.whTime(145)

s = merc.whCurVal(145, 0)
t1 = merc.whCurVal(145, 1)
t2 = merc.whCurVal(145, 2)

sf = merc.whFixDay(145, 0, 0)
t1f = merc.whFixDay(145, 1, 0)
t2f = merc.whFixDay(145, 2, 0)

sfm = merc.whFixMonth(145, 5, 0)
t1fm = merc.whFixMonth(145, 5, 1)
t2fm = merc.whFixMonth(145, 5, 2)
'''
#m = merc.whMPLR(145)
#mv = merc.whMPVal(145, '00', '00')
#m = merc.whMPDVal(145, 1000)

#for i in m.values():
#    print '-----------------------------------------------------------------------'
#    print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
    
#print len(m)
'''
print 'WH Number %s' % (n)
print 'WH Time: %s Season: %s' % (t['DateTime'], t['Season'])
print '-------------------------------------------------------------'
print 'Wh currents: A: %.2f    R: %.2f' % (s['A'], s['R'])
print 'Wh T1: A: %.2f    R: %.2f' % (t1['A'], t1['R'])
print 'Wh T2: A: %.2f    R: %.2f' % (t2['A'], t2['R'])
print '-------------------------------------------------------------'
print 'Wh fixed today: A: %.2f    R: %.2f' % (sf['A'], sf['R'])
print 'Wh T1: A: %.2f    R: %.2f' % (t1f['A'], t1f['R'])
print 'Wh T2: A: %.2f    R: %.2f' % (t2f['A'], t2f['R'])
print '-------------------------------------------------------------'
print 'Wh fixed month: A: %.2f    R: %.2f' % (sfm['A'], sfm['R'])
print 'Wh T1: A: %.2f    R: %.2f' % (t1fm['A'], t1fm['R'])
print 'Wh T2: A: %.2f    R: %.2f' % (t2fm['A'], t2fm['R'])
'''
'''
print '-------------------------------------------------------------'
print '\
 HiByte: %s\n \
LoByte: %s\n \
Status: %s\n \
DateTime: %s.%s.%s %s:%s\n \
Period: %d\n \
' % (m['HiB'], m['LoB'], m['Status'], m['d'], m['m'], m['y'], m['H'], m['M'], m['Period'])
'''
#print ml

#stp = time.strptime(m['d']+m['m']+m['y']+m['H']+m['M'], '%d%m%y%H%M')
#print stp
#print time.strftime('%d.%m.%y %H:%M:%S', stp)