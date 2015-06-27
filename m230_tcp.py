#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from m230_class import m230
from dev_channel import DirectChannel as DC
from dev_channel import GSMChannel as GSM
from dev_channel import TCPChannel as TCP




wh_adr_set_list = [34,]

channel = TCP(address = '192.168.0.123', attempt = 3, port = 55556, whTimeout=5)
#channel = TCP(address = '192.168.0.122', port = 15555, whTimeout=15)



merc = m230(channel)

for wh_adr_set in wh_adr_set_list:
	
	if merc.whAuth(wh_adr_set, 111111, 1):
		print 'WhNum: ' + merc.whNum(wh_adr_set)
		En = merc.whCurVal(wh_adr_set)
		if En:
			print 'Total: A - %.2f, R - %.2f' % (En['A'], En['R'])
		EnF = merc.whFixDay(wh_adr_set)
		if EnF:
			print 'Total: A - %.2f, R - %.2f' % (EnF['A'], EnF['R'])
			print 'Diff today: %.2f' % (En['A'] - EnF['A'])
		else:
			print u'Не удалось выполнить чтение!'
			
		Profile = merc.whPPDepthValue(wh_adr_set, 10)
		
		
		"""
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
		"""
		merc.whLogOut(wh_adr_set)
	else:
		print 'Счетчик с адресом %s, не отвечает' % wh_adr_set
	
channel.terminate()

"""
wh_adr_set_list1 = [34]

channel1 = TCP(address = '192.168.0.123', attempt = 3, port = 55556, whTimeout=10)
#channel = TCP(address = '192.168.0.122', port = 15555, whTimeout=15)



merc1 = m230(channel1)

for wh_adr_set1 in wh_adr_set_list1:
	
	if merc1.whAuth(wh_adr_set1, 111111, 1):
		print 'WhNum: ' + merc1.whNum(wh_adr_set1)
		En = merc1.whCurVal(wh_adr_set1)
		if En:
			print 'Total: A - %.2f, R - %.2f' % (En['A'], En['R'])
		EnF = merc1.whFixDay(wh_adr_set1)
		if EnF:
			print 'Total: A - %.2f, R - %.2f' % (EnF['A'], EnF['R'])
			print 'Diff today: %.2f' % (En['A'] - EnF['A'])
		else:
			print u'Не удалось выполнить чтение!'
			
		Profile = merc1.whPPDepthValue(wh_adr_set1, 10)
		
		
	
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
		
		merc1.whLogOut(wh_adr_set1)
	else:
		print 'Счетчик с адресом %s, не отвечает' % wh_adr_set1
	
channel1.terminate()
"""