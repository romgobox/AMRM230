#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import serial
import time
import datetime
from CRC16 import CRC16
#from gsm import whCall, whCallTerm


def whCall(portObj, num='', timeWA=10):
    callCmd = 'ATD'+num+'\r'
    print 'Calling '+num+'...'
    portObj.write(callCmd)        
    answer =''
    rx=True
    while rx==True:
        answer += portObj.read(portObj.inWaiting())
        #time.sleep(0.1)
        if 'CONNECT 9600' in answer:
            rx=False
        elif 'NO CARRIER' in answer:
            rx=False
    print answer
    
    if 'CONNECT 9600' in answer:
        return True
    else:
        return False
    time.sleep(timeWA)
        
        
    
def whCallTerm(portObj, timeWA=3):
    time.sleep(timeWA)
    print "+++"
    portObj.write('+++')
    time.sleep(timeWA)
    print "ATH"
    portObj.write('ATH\r')
    return True


class m230():
    def __init__(self, port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1, writeTimeout=1, ser = serial.Serial(), whTimeout = 0.1):
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
    
        try:
            self.ser.open()
        except Exception:
            print 'Port not found: ' + self.port
        else:
            print 'Port opened'
    '''
    def cmdWR(self, cmd, CRC=CRC16(True)):
        send = cmd + CRC.calculate(cmd)
        cmdsend = [self.chSim(hex(ord(x))[2:]) for x in send]
        print self.udate()+' >>> ' + " ".join(cmdsend)
        self.ser.write(send)
        time.sleep(self.whTimeout)
        
        answer = []
        rx=3
        while rx>0:
            
            answer += [self.chSim(hex(ord(x))[2:]) for x in self.ser.read(self.ser.inWaiting())]
            if len(answer)>2:
                rx=0
                print self.udate()+' <<< ' + " ".join(answer)
            else:
                rx=rx-1
                print self.udate()+' >>> ' + " ".join(cmdsend)
                self.ser.write(send)
                time.sleep(self.whTimeout)
        
        return answer
        time.sleep(self.whTimeout)
    '''
    def cmdWR(self, cmd, CRC=CRC16(True)):
        send = cmd + CRC.calculate(cmd)
        cmdsend = [self.chSim(hex(ord(x))[2:]) for x in send]
        print self.udate()+' >>> ' + " ".join(cmdsend)
        self.ser.write(send)
        #time.sleep(self.whTimeout)
        
        answer = []
        ans=''
        rx=3
        timeO=0
        while rx>0:
            while timeO < self.whTimeout:
                time.sleep(0.1)
                ans += self.ser.read(self.ser.inWaiting())
                answer += [self.chSim(hex(ord(x))[2:]) for x in ans]
                if self.chCRC(ans):
                    timeO = self.whTimeout
                    rx=0
                    print self.udate()+' <<< ' + " ".join(answer)
                else:
                    timeO+=0.1
            if not self.chCRC(ans):
                rx=rx-1
                timeO=0
                print self.udate()+' >>> ' + " ".join(cmdsend)
                self.ser.write(send)
                #time.sleep(self.whTimeout)
        
        return answer
        #time.sleep(self.whTimeout)
        
    # Метод для авторизации в приборе учета (ПУ). Принимает в качестве параметров сетевой адрес ПУ
    # (значение int, для Меркурий 230 в диапазоне 1 - 240, на адрес 0 отвечает любой прибор учета на шине,
    # не рекомендуется использовать с группой счетчиков), пароль 1-го или 2-го уровня доступа, уровень доступа
    # (1-й чтение информации, 2-й чтение и запись параметров)
    def whAuth(self, whAdr=0, whPass=111111, whLevAuth=1):
        whPass_chr = ''.join([chr(int(x)) for x in str(whPass)])
        authCmd = chr(whAdr) + '\x01' + chr(whLevAuth) + whPass_chr
        self.cmdWR(authCmd)
  
    # Метод предназначен для чтения серийного номера прибора учета
    # возвращает номер в виде строки
    def whNum(self, whAdr=0):
        self.whAdr = chr(whAdr)
        ans = self.cmdWR(self.whAdr + '\x08\x00')
        self.whN = [str(int(x, 16)) for x in ans[1:5]]
        return "".join(self.whN)
        
    # Метод предназначен для чтения даты, времени и признака сезона
    # возвращает словарь с ключами 'DateTime' - дату, время в доступном для стандартного форматирования виде,
    # а также 'Season' - признак сезона 1-зима, 0-лето
    # Принимает в качетсве параметров сетевой адрес прибора учет,
    # формат даты и времени
    def whTime(self, whAdr=0, datetimefrmt='%d.%m.%y %H:%M:%S'):
        self.whAdr = chr(whAdr)
        self.datetimefrmt = datetimefrmt
        ans = self.cmdWR(self.whAdr + '\x04\x00')
        self.time_tuple = [int(x) for x in ans[5:8]][::-1] + [int(x) for x in ans[1:4]][::-1] + [0,1] + [int(ans[-3])]
        self.whDateForm = time.strftime(self.datetimefrmt, self.time_tuple)
        self.whSeason = int(ans[-3])
        self.whDateTime = {'DateTime': self.whDateForm, 'Season': self.whSeason}
        return self.whDateTime
    
    # Метод предназначен для чтения текущих показаний ПУ (от сброса) всего или по тарифам
    # возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
    # Принимает в качетсве параметров сетевой адрес прибора учет, номер тарифа (значение по-умолчанию 00-суммарная энергия)
    def whCurVal(self, whAdr=0, whT=00):
        self.whAdr = chr(whAdr)
        self.whT = chr(whT)
        ans = self.cmdWR(self.whAdr + '\x05\x00' + self.whT)
        self.whCurA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.001
        self.whCurR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.001
        self.whCur = {'A':self.whCurA, 'R':self.whCurR}
        return self.whCur
    
    # Метод предназначен для чтения зафиксированных показаний ПУ на начало суток всего или по тарифам
    # возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
    # Принимает в качетсве параметров сетевой адрес прибора учет, номер тарифа (значение по-умолчанию 0-суммарная энергия),
    # currentday: 1 - текущие сутки, 0 - предыдущие сутки
    def whFixDay(self, whAdr=0, whT=0, currentday=1):
        self.whAdr = chr(whAdr)
        self.whT = whT
        self.currentday = currentday
        if self.currentday == 1:
            self.valAdr = {0:'\x06\xA6', 1:'\x06\xB7', 2:'\x06\xC8', 3:'\x06\xD9', 4:'\x06\xEA'}
        elif self.currentday == 0:
            self.valAdr = {0:'\x06\xFB', 1:'\x07\x0C', 2:'\x07\x1D', 3:'\x07\x2E', 4:'\x07\x3F'}
        else:
            print 'value currentday must be 1 for current day or 0 for previous day'

        ans = self.cmdWR(self.whAdr + '\x06\x02' + self.valAdr[self.whT] + '\x10')
        self.whFixA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
        self.whFixR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
        self.whFix = {'A':self.whFixA, 'R':self.whFixR}
        return self.whFix
    
    # Метод предназначен для чтения зафиксированных показаний ПУ за на начало месяца всего или по тарифам
    # возвращает словарь с ключами 'A', 'R' - значение активной/реактивной энергии
    # Принимает в качетсве параметров сетевой адрес прибора учет, месяц (по-умолчанию текущий) номер тарифа (значение по-умолчанию 0-суммарная энергия),
    def whFixMonth(self, whAdr=0, month=int(datetime.datetime.now().strftime("%m")), whT=0):
        self.whAdr = chr(whAdr)
        self.whT = whT
        self.month = month
        self.valAdr = {
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
        if self.month == int(datetime.datetime.now().strftime("%m")): self.month = int(datetime.datetime.now().strftime("%m"))
        ans = self.cmdWR(self.whAdr + '\x06\x02' + self.valAdr[self.month][self.whT] + '\x10')
        self.whFixMA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
        self.whFixMR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
        self.whFixM = {'A':self.whFixMA, 'R':self.whFixMR}
        return self.whFixM
    
    # Метод предназначен для чтения адреса последней записи средних мощностей,
    # возвращает словарь с ключами:
    #            'HiB' - старший байт адреса
    #            'LoB' - младший байт адреса
    #            'Status' - байт-статус записи (см. описание протокола)
    #            'H' - час фиксации
    #            'M' - минута фиксации
    #            'd' - день фиксации
    #            'm' - месяц фиксации
    #            'y' - год фиксации
    #            'Period' - период интегрирования мощности
    # Принимает в качетсве параметров сетевой адрес прибора учет
    def whMPLR(self, whAdr=0):
        self.whAdr = chr(whAdr)
        ans = self.cmdWR(self.whAdr + '\x08\x13')
        self.MPLR = {
                'HiB':ans[1],
                'LoB':ans[2],
                'Status':bin(int(ans[3], 16))[2:],
                'H':self.chSim(ans[4]),
                'M':self.chSim(ans[5]),
                'd':self.chSim(ans[6]),
                'm':self.chSim(ans[7]),
                'y':self.chSim(ans[8]),
                'Period':int(ans[9], 16),
                }
        return self.MPLR
    
    # Метод предназначен для чтения записи средних мощностей по определенному адресу,
    # возвращает словарь с ключами:
    #            'Status' - байт-статус записи (см. описание протокола)
    #            'H' - час фиксации
    #            'M' - минута фиксации
    #            'd' - день фиксации
    #            'm' - месяц фиксации
    #            'y' - год фиксации
    #            'Period' - период интегрирования мощности
    #            'A' - активная мощность
    #            'R' - реактивная мощность
    # Принимает в качетсве параметров сетевой адрес прибора учет, старший байт адреса, младший байт адреса
    def whMPVal(self, whAdr=0, HiB='00', LoB='00'):
        self.whAdr = chr(whAdr)
        self.HiB = HiB
        self.LoB = LoB
        self.chByte = lambda x: chr(int(x, 16))
        ans = self.cmdWR(self.whAdr + '\x06\x03' + self.chByte(self.HiB) + self.chByte(self.LoB) + '\x0F')
        self.MPVal = {
                'Status':bin(int(ans[1], 16))[2:],
                'H':self.chSim(ans[2]),
                'M':self.chSim(ans[3]),
                'd':self.chSim(ans[4]),
                'm':self.chSim(ans[5]),
                'y':self.chSim(ans[6]),
                'Period':int(ans[7], 16),
                'A':int(ans[9]+ans[8], 16)*0.001,
                'R':int(ans[13]+ans[12], 16)*0.001
                }
        return self.MPVal
    
    # Метод предназначен для чтения записи средних мощностей на определенную глубину,
    # возвращает словарь с ключами:
    #            'Status' - байт-статус записи (см. описание протокола)
    #            'H' - час фиксации
    #            'M' - минута фиксации
    #            'd' - день фиксации
    #            'm' - месяц фиксации
    #            'y' - год фиксации
    #            'Period' - период интегрирования мощности
    #            'A' - активная мощность
    #            'R' - реактивная мощность
    # Принимает в качетсве параметров сетевой адрес прибора учет, глубину опроса
    def whMPDVal(self, whAdr=0, deep=1):
        self.deep = deep
        self.MPDVal = {}
        self.lastMPLR = self.whMPLR(whAdr)
        self.ADR = int(self.lastMPLR['HiB']+self.lastMPLR['LoB'], 16)
        for i in range(0, self.deep):
            self.ADRH = hex(self.ADR)[2:]
            self.ADRres = {
                1: '0000',
                2: '00'+str(self.ADRH[0:]),
                3: '0'+str(self.ADRH[0:]),
                4: str(self.ADRH[0:])
            }.get(len(self.ADRH))
            self.ADRHi = self.ADRres[0:2]
            self.ADRLo = self.ADRres[2:]
            ans = self.whMPVal(whAdr, self.ADRHi, self.ADRLo)
            self.MPDVal[i] = ans
            #print i, self.ADRHi, self.ADRLo
            self.ADR = self.ADR - 16
            if self.ADR == 0: self.ADR = 65520
        return self.MPDVal
        
    
    ###################################################################
    def chSim(self, sim):
        self.sim = sim
        if len(self.sim)==1: self.sim = "0" + self.sim
        return self.sim
    
    def udate(self):
        return datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S.%f")
    ###################################################################
    
    def chCRC(self, cmd, CRC=CRC16(True)):
        if CRC.calculate(cmd[:-2]) == cmd[-2:]:
            return True
        else:
            return False
        
wh_adr_set = 145
wh_adr_set1 = 43
merc = m230('/dev/ttyUSB0', whTimeout=5)

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




