#Version 0.1
#Author: Harshavardhan Anne

import serial

class MA200(object):
    _baudrate = 1000000
    _port = '/dev/ttyUSB0'
    _serialObj = serial.Serial()
    _status_flag = 1
    _print_option = 0   #0 = No printing, 1 = console printing
    _data_buff = None
    _status_codes = {"1"   : "No status notifications",
                     "2"   : "Instrument in sampling and measurement startup",
                     "4"   : "Tape advance occurring during sampling and measurement period",
                     "8"   : "N/A",
                     "16"  : "Optical saturation",
                     "32"  : "Sampling timing error",
                     "64"  : "Sampling spot 2 of DualSpot loading compensation is active",
                     "128" : "Flow unstable during sampling and measurement period. Flow deviates from target flow setpoint by more than +/- 5%",
                     "256" : "Flow out of range during sampling and measurement period",
                     "512" : "Time synchronization is manual (synchronized to application/computer time)"}

    def __init__(self,port,print_opt=None):
        self._port = port

        if print_opt is None:
            self._print_option = 0
        elif print_opt == 1:
            self._print_option = print_opt
        else:
            print ("(MA200O): Error: print_option invalid")
            self._print_option = 0

    def open(self):
        if (self._print_option): print "(MA200): Initializing device"
        self._serialObj.baudrate = self._baudrate
        self._serialObj.port = self._port
        self._serialObj.bytesize = serial.EIGHTBITS
        self._serialObj.parity = serial.PARITY_NONE
        self._serialObj.stopbits = serial.STOPBITS_ONE
        self._serialObj.xonxoff = False
        self._serialObj.timeout = 0.3
        self._serialObj.write_timeout = 0.3

        try:
            self._serialObj.open()
            if (self._print_option): print "(MA200): Serial connection established"
            self._status_flag = 0

        except serial.serialutil.SerialException:
            if (self._print_option): print "(MA200): Could not open serial port %s" % self._port
            self._status_flag = 1

    def close(self):
        self._status_flag = 1
        try:
            self._serialObj.close()
            if (self._print_option): print ("(MA200): Successfully closed serial port")
        except:
            if (self._print_option): print ("(MA200): Could not close port")

    def read(self):
        if self._serialObj.is_open == True:
            if self._status_flag == 0:
                if (self._print_option): print ("(MA200): Attempting to reading data")
                try:
                    temp = self._serialObj.readline()
                    if temp[0:5] == 'MA200':
                        self._data_buff = temp.rstrip('\r\n')
                        if (self._print_option): print ("(MA200): Data received")
                        return self._data_buff
                    else:
                        return None
                except Exception as e:
                    if (self._print_option): print ("(MA200): Exception!!!")
                    print (e)
                    self._status_flag = 1
                    return None

    def get_status(self):
        return self._status_flag

    def get_most_recent(self):
        return self._data_buff

    def get_status_code(self,*args):
        li = []
        for arg in args:
            li.append(self._status_codes.get(arg,None))
        return li
