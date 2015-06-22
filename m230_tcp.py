#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from m230_class import m230
from dev_channel import DirectChannel as DC
from dev_channel import GSMChannel as GSM
from dev_channel import TCPChannel as TCP




wh_adr_set_list = [29,]

channel = TCP(address = '192.168.0.123', port = 55555, whTimeout=15)
#channel = TCP(address = '192.168.0.122', port = 15555, whTimeout=15)



merc = m230(channel)

for wh_adr_set in wh_adr_set_list:
	
	if merc.whAuth(wh_adr_set, 111111, 1):
		print 'WhNum: ' + merc.whNum(wh_adr_set)
		En = merc.whCurVal(wh_adr_set)
		print 'Total: A - %s, R - %s' % (En['A'], En['R'])

		U = merc.whU(wh_adr_set)
		
		
		
		A = merc.whUAngle(wh_adr_set)
		
		
		
		I = merc.whI(wh_adr_set)
		
		
		C = merc.whCosf(wh_adr_set)
		
		
		P = merc.whP(wh_adr_set, en='P')
		
		print 'Wh: %s' % wh_adr_set
		print 'U1: %s, U2: %s U3: %s' % (U[1],U[2],U[3],)
		print "I1: " + str(I[1]) + " I2: " + str(I[2]) + " I3: " + str(I[3])
		print 'C0: %.2f, C1: %.2f, C2: %.2f C3: %.2f' % (C[0], C[1],C[2],C[3],)
		print 'P0: %.2f, P1: %.2f, P2: %.2f P3: %.2f' % (P[0], P[1],P[2],P[3],)
		print 'A12: %s, A13: %s A23: %s' % (A[12],A[13],A[23],)
		merc.whLogOut(wh_adr_set)
	else:
		print 'Счетчик с адресом %s, не отвечает' % wh_adr_set
	
channel.terminate()

	
