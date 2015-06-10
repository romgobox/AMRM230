#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
#import serial
import time
import datetime

from CRC16 import CRC16
from utils import chSim, udate





class m230():
  
    def __init__(self, channel, CRC=CRC16(True)):
        self.channel = channel
        self.CRC = CRC

    def cmdWR(self, cmd):
        
        
        send = cmd
        cmdsend = [chSim(hex(ord(x))[2:]) for x in send]
        print udate()+' >>> ' + " ".join(cmdsend)
        self.channel.TX(send)
        
        self.whTimeout = self.channel.whTimeout
        
        answer = []
        ans=''
        rx=3
        timeO=0
        while rx>0:
            while timeO < self.whTimeout:
                time.sleep(0.1)
                ans += self.channel.RX()
                answer += [chSim(hex(ord(x))[2:]) for x in ans]
                if self.chCRC(ans):
                    timeO = self.whTimeout
                    rx=0
                    print udate()+' <<< ' + " ".join(answer)
                else:
                    timeO+=0.1
            if not self.chCRC(ans):
                rx=rx-1
                timeO=0
                print udate()+' >>> ' + " ".join(cmdsend)
                self.channel.TX(send)
                #time.sleep(self.whTimeout)
     
        
        return answer
        #time.sleep(self.whTimeout)
        

    def whAuth(self, whAdr=0, whPass=111111, whLevAuth=1):
        """
        Метод для авторизации в приборе учета (ПУ). Принимает в качестве параметров сетевой адрес ПУ
        (значение int, для Меркурий 230 в диапазоне 1 - 240, на адрес 0 отвечает любой прибор учета на шине,
        не рекомендуется использовать с группой счетчиков), пароль 1-го или 2-го уровня доступа, уровень доступа
        (1-й чтение информации, 2-й чтение и запись параметров)
        """
        
        whPass_chr = ''.join([chr(int(x)) for x in str(whPass)])
        cmd = chr(whAdr) + '\x01' + chr(whLevAuth) + whPass_chr
        authCmd = cmd + self.CRC.calculate(cmd)
        authAns = self.cmdWR(authCmd)
        chAns=[]
        readyAns = chr(whAdr) + '\x00' + self.CRC.calculate(chr(whAdr) + '\x00')
        chAns += [chSim(hex(ord(x))[2:]) for x in readyAns]
        
        if authAns == chAns:
            print u'Соединение со счетчиком %s и паролем %s установлено!' % (str(whAdr), str(whPass))
        else:
            print u'Не удалось установить соединение со счетчиком '+ str(whAdr)
    
    def whLogOut(self, whAdr=0):
        """
        Метод для завершения соединения со счетчиком
        """
        cmd = chr(whAdr) + '\x02'
        logOutCmd = cmd + self.CRC.calculate(cmd)
        logOutAns = self.cmdWR(logOutCmd)
        
    def whNum(self, whAdr=0):
        """
        Метод предназначен для чтения серийного номера прибора учета
        возвращает номер в виде строки
        """
        
        cmd = chr(whAdr) + '\x08\x00'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        whN = [str(int(x, 16)) for x in ans[1:5]]
        return "".join(whN)
        
   
    def whTime(self, whAdr=0, datetimefrmt='%d.%m.%y %H:%M:%S'):
        """
        Метод предназначен для чтения даты, времени и признака сезона
        возвращает словарь с ключами 'DateTime' - дату, время в доступном для стандартного форматирования виде,
        а также 'Season' - признак сезона 1-зима, 0-лето
        Принимает в качетсве параметров сетевой адрес прибора учет, формат даты и времени
        """
        
        cmd = chr(whAdr) + '\x04\x00'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        time_tuple = [int(x) for x in ans[5:8]][::-1] + [int(x) for x in ans[1:4]][::-1] + [0,1] + [int(ans[-3])]
        whDateForm = time.strftime(datetimefrmt, time_tuple)
        whSeason = int(ans[-3])
        whDateTime = {'DateTime': whDateForm, 'Season': whSeason}
        return whDateTime
    
    def whCurVal(self, whAdr=0, whT=00):
        """
        Метод предназначен для чтения текущих показаний ПУ (от сброса) всего или по тарифам
        возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
        Принимает в качетсве параметров сетевой адрес прибора учет, номер тарифа (значение по-умолчанию 00-суммарная энергия)
        """
        
        cmd = chr(whAdr) + '\x05\x00' + chr(whT)
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        whCurA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.001
        whCurR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.001
        whCur = {'A':whCurA, 'R':whCurR}
        return whCur
    
    
    def whFixDay(self, whAdr=0, whT=0, currentday=1):
        """
        Метод предназначен для чтения зафиксированных показаний ПУ на начало суток всего или по тарифам
        возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
        Принимает в качетсве параметров сетевой адрес прибора учет, номер тарифа (значение по-умолчанию 0-суммарная энергия),
        currentday: 1 - текущие сутки, 0 - предыдущие сутки
        """

        if currentday == 1:
            valAdr = {0:'\x06\xA6', 1:'\x06\xB7', 2:'\x06\xC8', 3:'\x06\xD9', 4:'\x06\xEA'}
        elif currentday == 0:
            valAdr = {0:'\x06\xFB', 1:'\x07\x0C', 2:'\x07\x1D', 3:'\x07\x2E', 4:'\x07\x3F'}
        else:
            print 'value currentday must be 1 for current day or 0 for previous day'
            
        cmd = chr(whAdr) + '\x06\x02' + valAdr[whT] + '\x10'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        whFixA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
        whFixR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
        whFix = {'A':whFixA, 'R':whFixR}
        return self.whFix
    
    
    def whFixMonth(self, whAdr=0, month=int(datetime.datetime.now().strftime("%m")), whT=0):
        """
        Метод предназначен для чтения зафиксированных показаний ПУ на начало месяца, суммарно или по тарифам
        возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
        Принимает в качетсве параметров сетевой адрес прибора учет, месяц (по-умолчанию текущий) номер тарифа
        (значение по-умолчанию 0-суммарная энергия),
        """

        valAdr = {
            1:{0:'\x02\xAA', 1:'\x02\xBB', 2:'\x02\xCC', 3:'\x02\xDD', 4:'\x02\xEE'},
            2:{0:'\x02\xFF', 1:'\x03\x10', 2:'\x03\x21', 3:'\x03\x32', 4:'\x03\x43'},
            3:{0:'\x03\x54', 1:'\x03\x65', 2:'\x03\x76', 3:'\x03\x87', 4:'\x03\x98'},
            4:{0:'\x03\xA9', 1:'\x03\xBA', 2:'\x03\xCB', 3:'\x03\xDC', 4:'\x03\xED'},
            5:{0:'\x03\xFE', 1:'\x04\x0F', 2:'\x04\x20', 3:'\x04\x31', 4:'\x04\x42'},
            6:{0:'\x04\x53', 1:'\x04\x64', 2:'\x04\x75', 3:'\x04\x86', 4:'\x04\x97'},
            7:{0:'\x04\xA8', 1:'\x04\xB9', 2:'\x04\xCA', 3:'\x04\xDB', 4:'\x04\xEC'},
            8:{0:'\x04\xFD', 1:'\x05\x0E', 2:'\x05\x1F', 3:'\x05\x30', 4:'\x05\x41'},
            9:{0:'\x05\x52', 1:'\x05\x63', 2:'\x05\x74', 3:'\x05\x85', 4:'\x05\x96'},
            10:{0:'\x05\xA7', 1:'\x05\xB8', 2:'\x05\xC9', 3:'\x05\xDA', 4:'\x05\xEB'},
            11:{0:'\x05\xFC', 1:'\x06\xD0', 2:'\x06\x1E', 3:'\x06\x2F', 4:'\x06\x40'},
            12:{0:'\x06\x51', 1:'\x06\x62', 2:'\x06\x73', 3:'\x06\x84', 4:'\x06\x95'}
        }
        if month == int(datetime.datetime.now().strftime("%m")): month = int(datetime.datetime.now().strftime("%m"))
        cmd = chr(whAdr) + '\x06\x02' + valAdr[month][whT] + '\x10'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        whFixMA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
        whFixMR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
        whFixM = {'A':whFixMA, 'R':whFixMR}
        return whFixM
    
    
    def whMPLR(self, whAdr=0):
        """
        Метод предназначен для чтения адреса последней записи средних мощностей,
        возвращает словарь с ключами:
                    'HiB' - старший байт адреса
                    'LoB' - младший байт адреса
                    'Status' - байт-статус записи (см. описание протокола)
                    'H' - час фиксации
                    'M' - минута фиксации
                    'd' - день фиксации
                    'm' - месяц фиксации
                    'y' - год фиксации
                    'Period' - период интегрирования мощности
         Принимает в качетсве параметров сетевой адрес прибора учет
        """
        
        cmd = chr(whAdr) + '\x08\x13'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        MPLR = {
                'HiB':ans[1],
                'LoB':ans[2],
                'Status':bin(int(ans[3], 16))[2:],
                'H':chSim(ans[4]),
                'M':chSim(ans[5]),
                'd':chSim(ans[6]),
                'm':chSim(ans[7]),
                'y':chSim(ans[8]),
                'Period':int(ans[9], 16),
                }
        return MPLR
    
    
    def whMPVal(self, whAdr=0, HiB='00', LoB='00'):
        """
        Метод предназначен для чтения записи средних мощностей по определенному адресу,
        возвращает словарь с ключами:
                    'Status' - байт-статус записи (см. описание протокола)
                    'H' - час фиксации
                    'M' - минута фиксации
                    'd' - день фиксации
                    'm' - месяц фиксации
                    'y' - год фиксации
                    'Period' - период интегрирования мощности
                    'A' - активная мощность
                    'R' - реактивная мощность
        Принимает в качетсве параметров сетевой адрес прибора учет, старший байт адреса, младший байт адреса
        """
        

        chByte = lambda x: chr(int(x, 16))
        cmd = chr(whAdr) + '\x06\x03' + chByte(HiB) + chByte(LoB) + '\x0F'
        ans = self.cmdWR(cmd + self.CRC.calculate(cmd))
        MPVal = {
                'Status':bin(int(ans[1], 16))[2:],
                'H':chSim(ans[2]),
                'M':chSim(ans[3]),
                'd':chSim(ans[4]),
                'm':chSim(ans[5]),
                'y':chSim(ans[6]),
                'Period':int(ans[7], 16),
                'A':int(ans[9]+ans[8], 16)*0.001,
                'R':int(ans[13]+ans[12], 16)*0.001
                }
        return MPVal
    
    
    def whMPDVal(self, whAdr=0, deep=1):
        """
        Метод предназначен для чтения записи средних мощностей на определенную глубину,
        возвращает словарь с ключами:
                    'Status' - байт-статус записи (см. описание протокола)
                    'H' - час фиксации
                    'M' - минута фиксации
                    'd' - день фиксации
                    'm' - месяц фиксации
                    'y' - год фиксации
                    'Period' - период интегрирования мощности
                    'A' - активная мощность
                    'R' - реактивная мощность
        Принимает в качетсве параметров сетевой адрес прибора учет, глубину опроса
        """
        
        MPDVal = {}
        lastMPLR = self.whMPLR(whAdr)
        ADR = int(lastMPLR['HiB']+lastMPLR['LoB'], 16)
        for i in range(0, deep):
            ADRH = hex(ADR)[2:]
            ADRres = {
                1: '0000',
                2: '00'+str(ADRH[0:]),
                3: '0'+str(ADRH[0:]),
                4: str(ADRH[0:])
            }.get(len(ADRH))
            ADRHi = ADRres[0:2]
            ADRLo = ADRres[2:]
            ans = self.whMPVal(whAdr, ADRHi, ADRLo)
            MPDVal[i] = ans
            ADR = ADR - 16
            if ADR == 0: ADR = 65520
        return MPDVal
        
    def chCRC(self, cmd, CRC=CRC16(True)):
        if CRC.calculate(cmd[:-2]) == cmd[-2:]:
            return True
        else:
            return False
        





