#! /usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time
from datetime import datetime
import logging
#logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'communications.log')
logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-4s [%(asctime)s] %(message)s', level = logging.DEBUG)

from utils import chSim, udate

#test komodo cvs




class m230():
    """The class implements the basic protocol commands metering device Mercury 230
    
    Args:
    
        channel (object): an instance of an object that implements the transfer of information (direct channel, GSM (CSD), TCP / IP)
    """
    def __init__(self, channel):
        self.channel = channel

    def cmdWR(self, cmd):
        return self.channel.TXRX(cmd)

    def whAuth(self, whAdr=0, whPass=111111, whLevAuth=1):
        """Method for authorization in the metering device
        
        Sends command authorization in the metering device
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            whPass (int): password metering device, (default value: 111111).
            whLevAuth (int): the access level metering device, 1 - read data (default value), 2 - reading / writing data.
        
        Returns:
        
            bool: True, if the authentication is successful, False in any other case.
        
        Examples:
        
            >>> m230.whAuth (whAdr = 145, whPass = 111111, whLevAuth = 1)
            True
            
            >>> m230.whAuth (whAdr = 145, whPass = 111111, whLevAuth = 2)
            False
        """
        
        whPass_chr = ''.join([chr(int(x)) for x in str(whPass)])
        whAuthCmd = chr(whAdr) + '\x01' + chr(whLevAuth) + whPass_chr
        logging.debug(u'Соединение со счетчиком %s и паролем %s:' % (str(whAdr), str(whPass)))
        authAns = self.cmdWR(whAuthCmd)
        if authAns[0:2] == [hex(whAdr)[2:], '00']:
            logging.debug(u'Соединение со счетчиком %s и паролем %s установлено!' % (str(whAdr), str(whPass)))
            auth = True
        else:
            logging.error(u'Не удалось установить соединение со счетчиком %s' % str(whAdr))
            auth = False

        return auth
    
    def whLogOut(self, whAdr=0):
        """Method to close the connection with the meter
        
        Sends command to close the connection with the meter
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            
        
        Returns:
        
            bool: True.
        
        Examples:
        
            >>> m230.whLogOut (whAdr = 145)
        """

        logOutCmd = chr(whAdr) + '\x02'
        logOutAns = self.cmdWR(logOutCmd)
        return True
        
    def whNum(self, whAdr=0):
        """Method is intended to read the serial number of the metering device
        
        Sends command to read the serial number of the metering device
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
        
        Returns:
        
            str: device serial number as a string.
        
        Examples:
        
            >>> m230.whNum (whAdr = 145)
            11199145
        """
        
        whNumCmd = chr(whAdr) + '\x08\x00'
        ans = self.cmdWR(whNumCmd)
        try:
            whN = [str(int(x, 16)) for x in ans[1:5]]
            whNum = "".join(whN)
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение серийного номера прибора учета! Причина: %s' % e)
            whNum = False
        return whNum
        
   
    def whTime(self, whAdr=0, datetimefrmt='%d.%m.%y %H:%M:%S'):
        """Method is intended for reading the date, time and indication of the season
        
        Sends command to read the date, time and indication of the season
        Args:
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus
            datetimefrmt (str): datetime format as a string
        
        Returns:
            dict: with key: (type) value
                DateTime :(str) a string representation of a datetime, depending on the `datetimefrmt`
                TimeDiff :(int) time difference between device and server, in seconds
                Season :(int) indicates the season, 1 - winter time, 0 - summer time (`su-a-amer ti-a-ame...`)
        
        Examples:
        
            >>> whTime = m230.whTime(whAdr=145, datetimefrmt='%Y-%m-%d %H:%M:%S')
            >>> print 'Device datetime: %s, Season: %d, Time difference: %d' % (whTime['DateTime'], whTime['Season'], whTime['TimeDiff'])
            Device datetime: 2015-06-16 10:00:44, Season: 1, Time difference: 3523
        """
        
        whTimeCmd = chr(whAdr) + '\x04\x00'
        ans = self.cmdWR(whTimeCmd)
        try:
            time_tuple = [int(x) for x in ans[5:8]][::-1] + [int(x) for x in ans[1:4]][::-1] + [0,1] + [int(ans[-3])]
            whDateForm = time.strftime(datetimefrmt, time_tuple)
            whSeason = int(ans[-3])
            whTimeDelta = datetime.strptime(whDateForm, datetimefrmt) - datetime.now()
            whDateTime = {'DateTime': whDateForm, 'Season': whSeason, 'TimeDiff':whTimeDelta.seconds}
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение времени прибора учета! Причина: %s' % e)
            whDateTime = False
        return whDateTime
    
    def whCurVal(self, whAdr=0, whT=0):
        """Method is intended for reading current values of energy (total or by tariffs)
        
        Sends command to read the current values of energy (total or by tariffs)
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            whT (int): number of tariff, 0 - total (default value).
        
        Returns:
        
            dict: with key: (type) value.
                A :(float) active energy value.
                R :(float) reactive energy value.
                
        Examples:
        
            >>> totalEn = merc.whCurVal(whAdr=145, whT=0)
            >>> print 'Total energy A: %.2f R: %.2f' % (totalEn['A'], totalEn['R'])
            Total energy A: 276.11 R: 0.63
            
            >>> T1_En = merc.whCurVal(whAdr=145, whT=1)
            >>> print 'Tariff 1 energy A: %.2f R: %.2f' % (T1_En['A'], T1_En['R'])
            Tariff 1 energy A: 184.48 R: 0.27
            
            >>> T2_En = merc.whCurVal(whAdr=145, whT=2)
            >>> print 'Tariff 2 energy A: %.2f R: %.2f' % (T2_En['A'], T2_En['R'])
            Tariff 2 energy A: 91.63 R: 0.36
        """
        
        whCurValCmd = chr(whAdr) + '\x05\x00' + chr(whT)
        ans = self.cmdWR(whCurValCmd)
        try:
            whCurA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.001
            whCurR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.001
            #TODO: implements new key ['T'] for indicate the number of tariff in return dict
            whCur = {'A':whCurA, 'R':whCurR}
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение текущих показаний прибора учета! Причина: %s' % e)
            whCur = False
        return whCur
    
    
    def whFixDay(self, whAdr=0, whT=0, currentday=1):
        """Method is intended for reading fixed values of the day (total or by tariffs)
        
        Sends command to read the fixed values of the day (total or by tariffs)
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            whT (int): number of tariff, 0 - total (default value).
            currentday (int): 1 - current day (default value), 0 - last day
        
        Returns:
        
            dict: with key: (type) value.
                A :(float) active energy value.
                R :(float) reactive energy value.
                
        Examples:
            
            >>> totalEn = merc.whFixDay(whAdr=145, whT=0, currentday=1)
            >>> print 'Total energy, current day  A: %.2f R: %.2f' % (totalEn['A'], totalEn['R'])
            Total energy, current day  A: 276.11 R: 0.63

            >>> T1_En = merc.whFixDay(whAdr=145, whT=1, currentday=1)
            >>> print 'Tariff 1 energy, current day A: %.2f R: %.2f' % (T1_En['A'], T1_En['R'])
            Tariff 1 energy, current day A: 184.48 R: 0.27
            
            >>> totalEn = merc.whFixDay(whAdr=145, whT=0, currentday=0)
            >>> print 'Total energy, last day  A: %.2f R: %.2f' % (totalEn['A'], totalEn['R'])
            Total energy, last day  A: 276.11 R: 0.63
        """
        
        if currentday == 1:
            valAdr = {0:'\x06\xA6', 1:'\x06\xB7', 2:'\x06\xC8', 3:'\x06\xD9', 4:'\x06\xEA'}
        elif currentday == 0:
            valAdr = {0:'\x06\xFB', 1:'\x07\x0C', 2:'\x07\x1D', 3:'\x07\x2E', 4:'\x07\x3F'}
        else:
            print 'value currentday must be 1 for current day or 0 for previous day'
            
        whFixDayCmd = chr(whAdr) + '\x06\x02' + valAdr[whT] + '\x10'
        ans = self.cmdWR(whFixDayCmd)
        try:
            whFixA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
            whFixR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
            #TODO: implements new key ['T'] for indicate the number of tariff in return dict
            whFix = {'A':whFixA, 'R':whFixR}
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение зафиксированных показаний прибора учета на начало суток! Причина: %s' % e)
            whFix = False
        return whFix
    
    
    def whFixMonth(self, whAdr=0, whT=0, month=int(datetime.now().strftime("%m"))):
        """Method is intended for reading fixed values of the month (total or by tariffs)
        
        Sends command to read the fixed values of the month (total or by tariffs)
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            whT (int): number of tariff, 0 - total (default value).
            month (int): number of month (default value: current month).
        
        Returns:
        
            dict: with key: (type) value.
                A :(float) active energy value.
                R :(float) reactive energy value.
                
        
        Examples:
            
            >>> totalEn = merc.whFixMonth(whAdr=145, whT=0)
            >>> print 'Total energy, current month  A: %.2f R: %.2f' % (totalEn['A'], totalEn['R'])
            Total energy, current month  A: 276.11 R: 0.63
            
            >>> T1_En = merc.whFixMonth(whAdr=145, whT=1)
            >>> print 'Tariff 1 energy, current month A: %.2f R: %.2f' % (T1_En['A'], T1_En['R'])
            Tariff 1 energy, current month A: 184.48 R: 0.27
            
            >>> totalEn = merc.whFixMonth(whAdr=145, whT=0, month=5)
            >>> print 'Total energy, May  A: %.2f R: %.2f' % (totalEn['A'], totalEn['R'])
            Total energy, May  A: 276.11 R: 0.63
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
        whFixMonthCmd = chr(whAdr) + '\x06\x02' + valAdr[month][whT] + '\x10'
        ans = self.cmdWR(whFixMonthCmd)
        try:
            whFixMA = int(ans[2] + ans[1] + ans[4] + ans[3], 16) * 0.0005
            whFixMR = int(ans[10] + ans[9] + ans[12] + ans[11], 16) * 0.0005
            whFixM = {'A':whFixMA, 'R':whFixMR}
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение зафиксированных показаний прибора учета на начало месяца! Причина: %s' % e)
            whFixM = False
        return whFixM
    
    
    def whPPLastRecord(self, whAdr=0):
        """Method is intended for reading last record values of power profile
        
        Sends command to read the last record values of power profile
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
        
        Returns:
        
            dict: with key: (type) value.
                HiB :(str) high byte records addres.
                LoB :(str) low byte records addres.
                Status: (str) binary representation of records status (check protocol), e.g. 11001
                H: (str) records Hour fixation
                m: (str) records Minute fixation
                d: (str) records Day fixation
                m: (str) records Month fixation
                y: (str) records Year fixation
                Period: (int) power discreteness  
        
        Examples:
            
            >>> PPLR = merc.whPPLastRecord(whAdr=145)
            >>> print 'Last Record Status: %s, Period: %s, High Byte: %s, Low Byte: %s, DateTime: %s-%s-%s %s:%s' % \
                (PPLR['Status'], PPLR['Period'], PPLR['HiB'], PPLR['LoB'], PPLR['d'], PPLR['m'], PPLR['y'], PPLR['H'], PPLR['M'])
            Last Record Status: 11001, Period: 30, High Byte: 49, Low Byte: 30, DateTime: 16-06-15 12:30
        """
    
        whPPLRCmd = chr(whAdr) + '\x08\x13'
        ans = self.cmdWR(whPPLRCmd)
        try:
            PPLR = {
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
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение последней записи профиля мощности! Причина: %s' % e)
            PPLR = False
        return PPLR
    
    
    def whPPValue(self, whAdr=0, HiB='00', LoB='00'):
        """Method is intended for reading value of power profile by given record address
        
        Sends command to read the value of power profile by given record address
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            HiB (str): high byte records addres, default value - 00.
            LoB (str): low byte records addres, default value - 00.
        
        Returns:
        
            
            dict: with key: (type) value.
                HiB :(str) high byte records addres.
                LoB :(str) low byte records addres.
                Status: (str) binary representation of records status (check protocol), e.g. 11001.
                H: (str) records Hour fixation.
                m: (str) records Minute fixation.
                d: (str) records Day fixation.
                m: (str) records Month fixation.
                y: (str) records Year fixation.
                Period: (int) power discreteness.
                A :(float) active energy value.
                R :(float) reactive energy value.
        
        Examples:
            
            >>> PPVal = merc.whPPValue(whAdr=145, HiB='48', LoB='E0')
            >>> print 'Record Status: %s, Period: %s, A: %s, R: %s, DateTime: %s-%s-%s %s:%s' % \
            (PPVal['Status'], PPVal['Period'], PPVal['A'], PPVal['R'], PPVal['d'], PPVal['m'], PPVal['y'], PPVal['H'], PPVal['M'])
            Last Record Status: 1001, Period: 30, A: 0.0, R: 0.0, DateTime: 16-06-15 12:30
        """
        
        
        chByte = lambda x: chr(int(x, 16))
        whPPValCmd = chr(whAdr) + '\x06\x03' + chByte(HiB) + chByte(LoB) + '\x0F'
        ans = self.cmdWR(whPPValCmd)
        try:
            PPV = {
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
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение записи профиля мощности по адресу 0x%s%s! Причина: %s' % (HiB,LoB,e))
            PPV = False
        return PPV
    
    
    def whPPDepthValue(self, whAdr=0, depth=1):
        """Method is intended for reading value of power profile by given record address on given depth
        
        Sends command to read the value of power profile by given record address on given depth.
        Discreteness of power profile records - 0x10
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            depth (int): depth of requests, e.g. depth=48 equal for power profile for 24 hours ago.
        
        Returns:
        
            dict of dict: with key: (type) value.
                HiB :(str) high byte records addres.
                LoB :(str) low byte records addres.
                Status: (str) binary representation of records status (check protocol), e.g. 11001.
                H: (str) records Hour fixation.
                m: (str) records Minute fixation.
                d: (str) records Day fixation.
                m: (str) records Month fixation.
                y: (str) records Year fixation.
                Period: (int) power discreteness.
                A :(float) active energy value.
                R :(float) reactive energy value.
        
        Examples:
            
            >>> PPVal = merc.whPPDepthValue(whAdr=145, depth=48)
            >>> if PPVal:
                    for i in PPVal.values():
                        print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' % \
                        (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
                Status: 1001 DateTime: 16.06.15 14:30 Period: 30 A: 0.000 R: 0.000
        """
        
        PPDV = {}
        ADR = None
        try:
            PPLR = self.whPPLastRecord(whAdr)
            ADR = int(PPLR['HiB']+PPLR['LoB'], 16)
        except Exception, e:
            logging.error(u'Не удалось выполнить чтение последней записи профиля мощности для расчета глубины опроса! Причина: %s' % (e))
            PPDVres = False
   
        if ADR:    
            for i in range(0, depth):
                ADRH = hex(ADR)[2:]
                ADRres = {
                    1: '0000',
                    2: '00'+str(ADRH[0:]),
                    3: '0'+str(ADRH[0:]),
                    4: str(ADRH[0:])
                }.get(len(ADRH))
                ADRHi = ADRres[0:2]
                ADRLo = ADRres[2:]
                ans = self.whPPValue(whAdr, ADRHi, ADRLo)
                if ans:
                    PPDV[i] = ans
                else:
                    logging.error(u'Не удалось выполнить чтение записи профиля мощности по адресу 0x%s%s на шаге %d!' % (ADRHi,ADRLo,i))
                ADR = ADR - 16
                if ADR == 0: ADR = 65520
            PPDVres = PPDV
        return PPDVres


    def whU(self, whAdr):
        """Method is intended for reading instantaneous values of Voltage (V)
        
        Sends command to read the instantaneous values of Voltage (V)
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
        
        Returns:
        
            dict: with key: (type) value.
                1 :(float) phase 1 voltage.
                2 :(float) phase 2 voltage.
                3 :(float) phase 3 voltage.
                
        Examples:
        
            >>> U = merc.whU(whAdr=145)
            >>> print 'U1: %s, U2: %s U3: %s' % (U[1],U[2],U[3],)
            U1: 207.37 U2: 0.0 U3: 14.08
        """
        
        U = {}
        ph = {1:'\x11', 2:'\x12', 3:'\x13',}
        for p in ph:
            whUCmd = chr(whAdr) + '\x08\x11' + ph[p]
            ans = self.cmdWR(whUCmd)
            try:
                U[p] = int(ans[1]+ans[3]+ans[2], 16)*0.01
            except Exception, e:
                logging.error(u'Не удалось выполнить чтение значения напряжения фазы %d! Причина: %s' % (p,e))
                U[p] = None
        return U
    
    def whUAngle(self, whAdr):
        """Method is intended for reading angles between the voltages
        
        Sends command to read the angles between the voltages
        !!! Not tested on real device !!!
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
        
        Returns:
        
            dict: with key: (type) value.
                12 :(float) angle between phase 1 and 2 voltages.
                13 :(float) angle between phase 1 and 3 voltages.
                23 :(float) angle between phase 2 and 3 voltages.
                
        Examples:
        
            >>> A = merc.whUAngle(whAdr=145)
            >>> print 'A12: %s, A13: %s A23: %s' % (A[12],A[13],A[23],)
            A12: 120, A13: 240 A23: 120
        """
        ph = {12:'\x51', 13:'\x52', 23:'\x53',}
        UAn = {}
        for p in ph:
            whUAnCmd = chr(whAdr) + '\x08\x11' + ph[p]
            ans = self.cmdWR(whUAnCmd)
            if ans[0:4] != [hex(whAdr)[2:], 'ff', 'ff', 'ff']:
                try:
                    UAn[p] = int(ans[1]+ans[3]+ans[2], 16)*0.01
                except Exception, e:
                    logging.error(u'Не удалось выполнить чтение значения угла между фазами %d! Причина: %s' % (p,e))
                    UAn[p] = None
            else:
                logging.error(u'Не удалось выполнить чтение значения угла между фазами %d! Причина: отсутствует нагрузка' % (p))
                UAn[p] = None
        return UAn

    
    def whI(self, whAdr):
        """Method is intended for reading instantaneous values of amperage (A)
        
        Sends command to read the instantaneous values of amperage (A)
        !!! Not tested on real device !!!
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
        
        Returns:
        
            dict: with key: (type) value.
                1 :(float) phase 1 amperage.
                2 :(float) phase 2 amperage.
                3 :(float) phase 3 amperage.
                
        Examples:
        
            >>> I = merc.whI(whAdr=145)
            >>> print 'I1: %s, I2: %s I3: %s' % (I[1],I[2],I[3],)
            I1: 1.37 I2: 2.0 I3: 1.08
        """
        ph = {1:'\x21', 2:'\x22', 3:'\x23',}
        I = {}
        for p in ph:
            whICmd = chr(whAdr) + '\x08\x11' + ph[p]
            ans = self.cmdWR(whICmd)
            try:
                I[p] = int(ans[1]+ans[3]+ans[2], 16)*0.001
            except Exception, e:
                logging.error(u'Не удалось выполнить чтение значения тока фазы %d! Причина: %s' % (p,e))
                I[p] = None
        return I
    
    def whP(self, whAdr, en='P'):
        """Method is intended for reading instantaneous values of power
        
        Sends command to read the instantaneous values of power
        !!! Not tested on real device !!!
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            en (str): type energy. P - active, Q - reactive, S - full 
        
        Returns:
        
            dict: with key: (type) value.
                0 :(float) total power.
                1 :(float) phase 1 power.
                2 :(float) phase 2 power.
                3 :(float) phase 3 power.
                
        Examples:
        
            >>> I = merc.whP(whAdr=145, en='P')
            >>> print 'P1: %.2f, P2: %.2f P3: %.2f' % (P[1],P[2],P[3],)
            P1: 0.00, P2: 0.00 P3: 0.00
        """
        ph = {
            'P':{0:'\x00', 1:'\x21', 2:'\x22', 3:'\x23',},
            'Q':{0:'\x04', 1:'\x05', 2:'\x06', 3:'\x07',},
            'S':{0:'\x08', 1:'\x09', 2:'\x0A', 3:'\x0B',},
        }
        P = {}
        for p in ph[en]:
            whPCmd = chr(whAdr) + '\x08\x11' + ph[en][p]
            ans = self.cmdWR(whPCmd)
            try:
                P[p] = int(ans[1]+ans[3]+ans[2], 16)*0.001
            except Exception, e:
                logging.error(u'Не удалось выполнить чтение значения мощности фазы %d! Причина: %s' % (p,e))
                P[p] = None
        return P
    
    def whCosf(self, whAdr, en='P'):
        """Method is intended for reading instantaneous values of power factor
        
        Sends command to read the instantaneous values of power factor
        !!! Not tested on real device !!!
        
        Args:
        
            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            en (str): type energy. P - active, Q - reactive, S - full 
            
        Returns:
        
            dict: with key: (type) value.
                0 :(float) total power.
                1 :(float) phase 1 power.
                2 :(float) phase 2 power.
                3 :(float) phase 3 power.
                
        Examples:
        
            >>> C = merc.whCosf(wh_adr_set)
            >>> print 'C1: %.2f, C2: %.2f C3: %.2f' % (C[1],C[2],C[3],)
            C1: 0.97 C2: 0.89 C3: 0.76
        """
        ph = {0:'\x30', 1:'\x31', 2:'\x32', 3:'\x33',}
        Cosf = {}
        for p in ph:
            whCosfCmd = chr(whAdr) + '\x08\x11' + ph[p]
            ans = self.cmdWR(whCosfCmd)
            try:
                Cosf[p] = int(ans[1]+ans[3]+ans[2], 16)*0.001
            except Exception, e:
                logging.error(u'Не удалось выполнить чтение значения к-та мощности фазы %d! Причина: %s' % (p,e))
                Cosf[p] = None
        return Cosf
    
    def whTestCMD(self, cmd='', useAdr=True, whAdr=0, Prefix='', HiB='', LoB='', Postfix=''):
        """Test method, for experiments. Developer only!
        """
        if useAdr:
            chByte = lambda x: chr(int(x, 16))
            whCmd = chr(whAdr) + Prefix + chByte(HiB) + chByte(LoB) + Postfix
            ans = self.cmdWR(whCmd)    
        else:
            ans = self.cmdWR(cmd)

        return ans
    
    def whMPDValFast(self, whAdr=0, deep=1):
        """Test method for fast power profile reading 
        """
        
        MPDVal = {}

        ADR = 0
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
            ans = self.whTestCMD('', True, whAdr, Prefix='\x06\x83', HiB=ADRHi, LoB=ADRLo, Postfix='\xD2')
            MPDVal[i] = ans
            ADR = ADR + 224
            if ADR == 65408: ADR = 0
        return MPDVal
      





