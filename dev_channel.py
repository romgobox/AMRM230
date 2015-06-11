#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
import datetime
import serial


from utils import chSim, udate
from CRC import CRC_M230


    
class DirectChannel(object):
    
    def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(), whTimeout = 0.1, whType=0):
        """
        Открывает прямой канал (как правило по протоколу RS-485) до счетчика.
        whType:
            0 - Меркурий 230
        """
        self.port = port
        self.ser = ser
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        self.ser.timeout = timeout
        self.ser.writeTimeout = writeTimeout
        self.whTimeout = whTimeout
        #self.whType = whType
        
        typeCRC = {
            0: CRC_M230(True),
        }
        self.CRC = typeCRC[whType]
        """
        """
    
        try:
            self.ser.open()
        except Exception:
            print u'Не удалось открыть порт: ' + self.port
        else:
            print u'Инициализация порта: ' + self.port
    
    def TXRX(self, cmd):
        answer = []
        ans=''
        send = cmd + self.CRC.calculate(cmd)
        cmdsend = [chSim(hex(ord(x))[2:]) for x in send]
        print udate()+' >>> ' + " ".join(cmdsend)
        self.TX(send)
        
        rx=3
        timeO=0
        while rx>0:
            while timeO < self.whTimeout:
                time.sleep(0.1)
                ans += self.RX()
                answer += [chSim(hex(ord(x))[2:]) for x in ans]
                if self.CRC.check(ans):
                    timeO = self.whTimeout
                    rx=0
                    print udate()+' <<< ' + " ".join(answer)
                else:
                    timeO+=0.1
            if not self.CRC.check(ans):
                rx=rx-1
                timeO=0
                print udate()+' >>> ' + " ".join(cmdsend)
                self.TX(send)
                #time.sleep(self.whTimeout)
     
        
        return answer
    
    """
    def chCRC(self, cmd, whType):
        typeCRC = {
            0: CRC(cmd, whType).chCRCM230
        }
        return typeCRC[whType]
    """    
    
    def TX(self, cmd):
        self.ser.write(cmd)
    
    def RX(self):
       return self.ser.read(self.ser.inWaiting())
    
    


