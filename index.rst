Module m230_class
-----------------

Classes
-------
m230 
    The class implements the basic protocol commands metering device Mercury 230

    Args:

        channel (object): an instance of an object that implements the transfer of information (direct channel, GSM (CSD), TCP / IP)

    Ancestors (in MRO)
    ------------------
    m230_class.m230

    Instance variables
    ------------------
    channel

    Methods
    -------
    __init__(self, channel)

    cmdWR(self, cmd)

    whAuth(self, whAdr=0, whPass=111111, whLevAuth=1)
        Method for authorization in the metering device

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

    whCosf(self, whAdr, en='P')
        Method is intended for reading instantaneous values of power factor

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

    whCurVal(self, whAdr=0, whT=0)
        Method is intended for reading current values of energy (total or by tariffs)

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

    whFixDay(self, whAdr=0, whT=0, currentday=1)
        Method is intended for reading fixed values of the day (total or by tariffs)

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

    whFixMonth(self, whAdr=0, whT=0, month=6)
        Method is intended for reading fixed values of the month (total or by tariffs)

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

    whI(self, whAdr)
        Method is intended for reading instantaneous values of amperage (A)

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

    whLogOut(self, whAdr=0)
        Method to close the connection with the meter

        Sends command to close the connection with the meter

        Args:

            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.
            

        Returns:

            bool: True.

        Examples:

            >>> m230.whLogOut (whAdr = 145)

    whMPDValFast(self, whAdr=0, deep=1)
        Test method for fast power profile reading

    whNum(self, whAdr=0)
        Method is intended to read the serial number of the metering device

        Sends command to read the serial number of the metering device

        Args:

            whAdr (int): the metering device address, for Mercury 230 from 1 to 240, 0 corresponds to the address of any device on the bus.

        Returns:

            str: device serial number as a string.

        Examples:

            >>> m230.whNum (whAdr = 145)
            11199145

    whP(self, whAdr, en='P')
        Method is intended for reading instantaneous values of power

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

    whPPDepthValue(self, whAdr=0, depth=1)
        Method is intended for reading value of power profile by given record address on given depth

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
                        print 'Status: %s DateTime: %s.%s.%s %s:%s Period: %d A: %.3f R: %.3f' %                         (i['Status'], i['d'], i['m'], i['y'], i['H'], i['M'], i['Period'], i['A'], i['R'])
                Status: 1001 DateTime: 16.06.15 14:30 Period: 30 A: 0.000 R: 0.000

    whPPLastRecord(self, whAdr=0)
        Method is intended for reading last record values of power profile

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
            >>> print 'Last Record Status: %s, Period: %s, High Byte: %s, Low Byte: %s, DateTime: %s-%s-%s %s:%s' %                 (PPLR['Status'], PPLR['Period'], PPLR['HiB'], PPLR['LoB'], PPLR['d'], PPLR['m'], PPLR['y'], PPLR['H'], PPLR['M'])
            Last Record Status: 11001, Period: 30, High Byte: 49, Low Byte: 30, DateTime: 16-06-15 12:30

    whPPValue(self, whAdr=0, HiB='00', LoB='00')
        Method is intended for reading value of power profile by given record address

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
            >>> print 'Record Status: %s, Period: %s, A: %s, R: %s, DateTime: %s-%s-%s %s:%s' %             (PPVal['Status'], PPVal['Period'], PPVal['A'], PPVal['R'], PPVal['d'], PPVal['m'], PPVal['y'], PPVal['H'], PPVal['M'])
            Last Record Status: 1001, Period: 30, A: 0.0, R: 0.0, DateTime: 16-06-15 12:30

    whTestCMD(self, cmd='', useAdr=True, whAdr=0, Prefix='', HiB='', LoB='', Postfix='')
        Test method, for experiments. Developer only!

    whTime(self, whAdr=0, datetimefrmt='%d.%m.%y %H:%M:%S')
        Method is intended for reading the date, time and indication of the season

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

    whU(self, whAdr)
        Method is intended for reading instantaneous values of Voltage (V)

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

    whUAngle(self, whAdr)
        Method is intended for reading angles between the voltages

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
