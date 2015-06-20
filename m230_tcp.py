#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from m230_class import m230
from dev_channel import DirectChannel as DC
from dev_channel import GSMChannel as GSM
from dev_channel import TCPChannel as TCP




wh_adr_set = 16

channel = TCP(address = '192.168.1.12', port = 5555, whTimeout=2)


merc = m230(channel)

if merc.whAuth(wh_adr_set, 111111, 1):
    print 'WhNum: ' + merc.whNum(wh_adr_set)
    merc.whLogOut(wh_adr_set)
    
channel.terminate()

    
