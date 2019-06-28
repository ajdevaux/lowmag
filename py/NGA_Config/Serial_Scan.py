import os
import serial
from serial.tools import list_ports
import io
import time

from NGA_Utils.Text_Config_Save import NGA_Text_Config_Save

'''
The class will identify which ports contain which piece of hardware
The Ardunio and MMC100 are both set to 38400 and will respond to the 1VER? command
Once connnected, will store information in a config_com_ports.txt file

'''

class NGA_Config_Serial_Scan:

    
    default_fake_port = 'COM0'
    default_serial_arduino = 'COM0';
    default_serial_MMC100 = 'COM0';
    default_serial_MFC2000 = 'COM0';
    default_serial_SMCPOLLUX = 'COM0';

    serial_arduino = default_serial_arduino
    serial_MMC100 = default_serial_MMC100
    serial_MFC2000 = default_serial_MFC2000
    serial_SMCPOLLUX = default_serial_SMCPOLLUX
    
    timeout_t = 0.1
    
    embedded = ""
    stage = ""

    def __init__(self):
        self.embedded = ""
        self.stage = ""
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
        
        self.serial_arduino = self.default_serial_arduino
        self.serial_MMC100 = self.default_serial_MMC100
        self.serial_MFC2000 = self.default_serial_MFC2000
        self.serial_SMCPOLLUX = self.default_serial_SMCPOLLUX
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
                    self.serial_MMC100 = port
                    
                if (port_found == False):
                    # 9600 baud for MFC-2000 (ASI Imaging)
                    ser = serial.Serial(port, 9600, timeout=self.timeout_t)
                    ser.write('\r') #send dummy command
                    self_id = ser.readline()
                    ser.write('WHO\r')
                    self_id = ser.readline()
                    #print self_id
                    ser.close()
                    # good response from MFC is ":A"
                    if ":A" == self_id[0:2]:
                        port_found = True
                        print "Config: Found: " + port + ": MFC-2000"
                        self.serial_MFC2000 = port
                
                if (port_found == False):
                    # 19200 for SMC Pollux (PI Micos)
                    ser = serial.Serial(port, 19200, timeout=self.timeout_t)
                    ser.write('3 nidentify\r')
                    self_id = ser.readline()
                    ser.close()
                    if "Pollux2" in self_id:
                        port_found = True
                        print "Config: Found: " + port + ": SMC-POLLUX"
                        self.serial_SMCPOLLUX = port
                        
                # Changed, FALSE -> 38400 for Arduino and MMC100 (Micronix)
                # Arduino now 9600 to allow LCD to work with SoftwareSerial at 9600
                if (port_found == False):
                    ser = serial.Serial(port, 38400, timeout=self.timeout_t)
                    # tried to get Arduino to not auto reset
                    # had to scratch RESET EN metal trace here to disable
                    # must short when reprogramming
                    #ser.setDTR(False)
                    #time.sleep(2)    # pause 2 seconds
                    #print ser.isOpen()
                    ser.write('\r') #send dummy command,
                    self_id = ser.readline().strip()
                    # let's us start a new command without garbage
                    # appears to be a bug in Arduino at 38400
                    ser.write('VER\r')
                    
                    self_id = ser.readline()
                    ser.close()
                    if  "NGA-LED-INT" in self_id:
                        port_found = True
                        print "Config: Found: " + port + ": NGA-LED-INT"
                        self.serial_arduino = port
            except:
                print "Config: COM Port Failed: " + port
            if port_found == False:
                print "Config: COM Port ignoring: " + port
                
        
        config_ports = dict()
        config_ports['arduino'] = self.serial_arduino
        config_ports['mmc100'] = self.serial_MMC100
        config_ports['mfc2000'] = self.serial_MFC2000
        config_ports['pollux'] = self.serial_SMCPOLLUX
        NGA_Text_Config_Save(r'..\config\config.com.ports.txt',config_ports)
        
        
        self.stage = 'virtual'
        selected_stage = dict()
        if (self.serial_MMC100 != self.default_fake_port and
                self.serial_SMCPOLLUX != self.default_fake_port):
            selected_stage['mmc_pollux_hybrid'] = self.serial_MMC100
            self.stage = 'mmc_pollux_hybrid'
        elif (self.serial_MFC2000 != self.default_fake_port and
                self.serial_SMCPOLLUX != self.default_fake_port):
            selected_stage['mfc_pollux_hybrid'] = self.serial_MFC2000
            self.stage = 'mfc_pollux_hybrid'
        elif (self.serial_MMC100 != self.default_fake_port):
            selected_stage['mmc100'] = self.serial_MMC100
            self.stage = 'mmc100'
        elif (self.serial_MFC2000 != self.default_fake_port):
            selected_stage['mfc2000'] = self.serial_MFC2000
            self.stage = 'mfc2000'
        elif (self.serial_SMCPOLLUX != self.default_fake_port):
            selected_stage['pollux'] = self.serial_SMCPOLLUX
            self.stage = 'pollux'
        else:
            selected_stage['virtual'] = self.default_fake_port
        NGA_Text_Config_Save(r'..\config\config.stage.defaults.txt',selected_stage)
        
        

