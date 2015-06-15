#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
import datetime
import serial
import logging
#logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'communications.log')
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG)

from utils import chSim, udate
from CRC import CRC_M230


    
class DirectChannel(object):
    
    def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(),\
                 whTimeout = 0.1, attempt = 3, whType=0):
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
        self.attempt = attempt
        
        typeCRC = {
            0: CRC_M230(True),
        }
        self.CRC = typeCRC[whType]
        """
        """
    
        try:
            self.ser.open()
        except Exception:
            logging.error(u'Не удалось открыть порт: ' + self.port)
        else:
            logging.debug(u'Инициализация порта: ' + self.port)
    
    def TXRX(self, cmd, byteExpected=0):
        ansHex = []
        ansChr=''
        
        self.attempt=3
        timeO=0
        
        while self.attempt>0:
            cmdTX = self.TX(cmd + self.CRC.calculate(cmd))
            logging.debug(u'TX >>> ' + " ".join(cmdTX[0]) + ' [' + str(cmdTX[1]) +'] ')
            
            while timeO < self.whTimeout:
                time.sleep(0.1)
                ansChr += self.RX()
                ansHex += [chSim(hex(ord(x))[2:]) for x in ansChr]
                
                if self.CRC.check(ansChr):
                    timeO = self.whTimeout
                    cmdRX = [ansHex, len(ansHex)]
                    logging.debug(u'RX <<< ' + " ".join(cmdRX[0]) + ' [' + str(cmdRX[1]) +'] ')
                else:
                    timeO += 0.1
            if self.CRC.check(ansChr):
                self.attempt = 0
                answer = ansHex
            else:
                self.attempt -= 1
                timeO = 0
                answer = u'Нет ответа от устройства!'
                logging.error(answer)
        return answer
    
    def TX(self, cmd):
        """
            Метод предназначен для отправки данных в порт
            Принимает в качестве параметров команду
            Возвращает список:
            cmdTX[0] - список, отправленная команда в 16-м представлении
            cmdTX[1] - количество отправленных байт
        """
        self.ser.write(cmd)
        cmdsend = [chSim(hex(ord(x))[2:]) for x in cmd]
        cmdTX = [cmdsend, len(cmdsend)]
        return cmdTX
        
    def RX(self):   
        return self.ser.read(self.ser.inWaiting())
    
    


