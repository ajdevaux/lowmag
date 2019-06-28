import os
import serial
from serial.tools import list_ports
import io
import time

'''
The class will identify which ports contain which piece of hardware
The Ardunio and MMC100 are both set to 38400 and will respond to the 1VER? command
Once connnected, will store information in a config_com_ports.txt file

'''

class Setup_Micronix_Stages:


    def __init__(self):
        self.embedded = ""
        self.stage = ""
        self.timeout_t = 1.0
        self.scan_ports()

    def serial_ports(self):
        """
        Returns a generator for all available serial ports
        """
        if os.name == 'nt':
            # windows
            for i in range(256):
                try:
                    s = serial.Serial(i)
                    s.close()
                    yield 'COM' + str(i + 1)
                except serial.SerialException:
                    pass
        else:
            # unix
            for port in list_ports.comports():
                yield port[0]


    def scan_ports(self):
        
        com_ports = list(self.serial_ports())
        print "Config: Scanning COM ports"
        for port in com_ports:
            port_found = False
            try:
                time.sleep(0.1)
                ser = serial.Serial(port, 38400, timeout=self.timeout_t)
                ser.write('1VER?\r')
                self_id = ser.readline()
                ser.close()
                if  "MMC-100" in self_id:
                    port_found = True
                    print "Config: Found: " + port + ": MMC-100"
                    self.setup_mmc100_port(port)
                        
            except:
                print "Config: COM Port Failed: " + port
            if port_found == False:
                print "Config: COM Port ignoring: " + port


    def send_commnd(self,ser,cmd):
        print "SENDING: " + cmd
        ser.write(cmd)
        time.sleep(0.1)
        
    def setup_mmc100_port(self, port):
        ser = serial.Serial(port, 38400, timeout=self.timeout_t)

##        self.send_commnd(ser,'1PGL1\r')
##        self.send_commnd(ser,'1MPL1\r')
##        self.send_commnd(ser,'1EPL1\r')
##        self.send_commnd(ser,'1FBK2\r')
##        self.send_commnd(ser,'1TLP25.0\r')
##        self.send_commnd(ser,'1TLN-25.0\r')
##        
##        self.send_commnd(ser,'1ERA1\r')
##        self.send_commnd(ser,'1PGM1\r')
##        self.send_commnd(ser,'1HOM\r')
##        self.send_commnd(ser,'1WST\r')
##        self.send_commnd(ser,'1WTM500\r')
##        self.send_commnd(ser,'1ZRO\r')
##        self.send_commnd(ser,'1END\r')
##
##        self.send_commnd(ser,'2PGL1\r')
##        self.send_commnd(ser,'2MPL0\r')
##        self.send_commnd(ser,'2EPL0\r')
##        self.send_commnd(ser,'2FBK2\r')
##        self.send_commnd(ser,'2TLP25.0\r')
##        self.send_commnd(ser,'2TLN-25.0\r')        
##
##        self.send_commnd(ser,'2ERA1\r')
##        self.send_commnd(ser,'2PGM1\r')
##        self.send_commnd(ser,'2HOM\r')
##        self.send_commnd(ser,'2WST\r')
##        self.send_commnd(ser,'2WTM500\r')
##        self.send_commnd(ser,'2ZRO\r')
##        self.send_commnd(ser,'2END\r')

        self.send_commnd(ser,'3PGL1\r')
        self.send_commnd(ser,'3MPL1\r')
        self.send_commnd(ser,'3EPL0\r')
        self.send_commnd(ser,'3FBK2\r')
        self.send_commnd(ser,'3TLP5.0\r')
        self.send_commnd(ser,'3TLN-5.0\r')        

        self.send_commnd(ser,'3ERA1\r')
        self.send_commnd(ser,'3PGM1\r')
        self.send_commnd(ser,'3HOM\r')
        self.send_commnd(ser,'3WST\r')
        self.send_commnd(ser,'3WTM500\r')
        self.send_commnd(ser,'3ZRO\r')
        self.send_commnd(ser,'3END\r')

        #self.send_commnd(ser,'1PGS1\r')
        #self.send_commnd(ser,'2PGS1\r')
        self.send_commnd(ser,'3PGS1\r')

        #self.send_commnd(ser,'1SAV\r')
        #self.send_commnd(ser,'2SAV\r')
        self.send_commnd(ser,'3SAV\r')
        
        ser.close()

if __name__ == '__main__':
    cfg = Setup_Micronix_Stages()
