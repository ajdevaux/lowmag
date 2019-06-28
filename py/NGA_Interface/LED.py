import serial

from NGA_Utils.Text_Config_Save import NGA_Text_Config_Save

from NGA_Config.LED import NGA_Config_LED

class NGA_Interface_LED:


    NOTHING = 'NOTHING'
    LED_OFF = 'LED_OFF'
    LED1_ON = 'LED1_ON'
    LED2_ON = 'LED2_ON'
    LED3_ON = 'LED3_ON'
    LED4_ON = 'LED4_ON'
    LED_ALL_ON = 'LED_ALL_ON'
    DUTY_CYCLE = 'DUTY_CYCLE'
    STATUS = 'STATUS'
    RESET_5V = 'RESET_5V'
    SERIAL_NUMBER = 'SERIAL_NUMBER'
    VERSION = 'VERSION'
    ERROR_CHECK = 'ERROR_CHECK'
    PRESSURE = 'PRESSURE'
    VACUUM_ON = 'VACUUM_ON'
    VACUUM_OFF = 'VACUUM_OFF'
    VALVE_ON = 'VALVE_ON'
    VALVE_OFF = 'VALVE_OFF'
    LCD1 = 'LCD1'
    LCD2 = 'LCD2'
    LCD3 = 'LCD3'
    LCD4 = 'LCD4'
    LCD5 = 'LCD5'
    LCD6 = 'LCD6'
    LCD7 = 'LCD7'
    led_config = None
    interface = ""
    success = True
    loaded = False
    led_on = [False, False, False, False]
    led_amp = [255, 255, 255, 255] # of 255
    vacuum_on = False
    valve_on = False
    pressure_measurement = 0 #psi
    cur_led_amp = 32
    arduino_port = 'COM0'
    arduino_com_speed = 38400 #was 38400, but changed to make LCD SoftwareSerial work

    def __init__(self, cmd = NOTHING):
        self.led_config = NGA_Config_LED()
        if 'arduino' in self.led_config.defaults.config:
            self.arduino_port = self.led_config.defaults.config['arduino']
            if (self.arduino_port != 'COM0'):
                try:
                    #connect to serial port
                    self.ser = serial.Serial(self.arduino_port, self.arduino_com_speed, timeout=0.5)
                    print "LED: Loaded"
                    self.loaded = True
                except:
                    print "LED: Not Loaded: Failed Connection, port: " + self.arduino_port
            else:
                print "LED: NOT Loaded: Not Found"
        else:
            self.arduino_port = 'COM0'
            print "LED: NOT Loaded: Not Configured"
        self.command(cmd)
        
        
    def __del__(self):
        self.close()

    def close(self):
        if (self.loaded == True):
            self.loaded = False
            self.ser.close()     

    def duty_cycle(self, ch, duty_cycle_in):
        if (duty_cycle_in > 0):
            if (duty_cycle_in < 255):
                self.led_amp[ch] = duty_cycle_in
            else:
                self.led_amp[ch] = 255
        else:
            self.led_amp[ch] = 0
        self.cur_led_amp = self.led_amp[ch]
        if (ch == 0):
            self.command(self.DUTY_CYCLE)
            self.command(self.LED1_ON)
        elif (ch == 1):
            self.command(self.DUTY_CYCLE)
            self.command(self.LED2_ON)
        elif (ch == 2):
            self.command(self.DUTY_CYCLE)
            self.command(self.LED3_ON)
        elif (ch == 3):
            self.command(self.DUTY_CYCLE)
            self.command(self.LED4_ON)

    def command_issue(self, cmd):
        if (cmd == self.NOTHING):
            self.ser.write('\r')
        if (cmd == self.LED1_ON):
            self.ser.write('L1\r')
            self.led_on[0] = True
        if (cmd == self.LED2_ON):
            self.ser.write('L2\r')
            self.led_on[1] = True
        if (cmd == self.LED3_ON):
            self.ser.write('L3\r')
            self.led_on[2] = True
        if (cmd == self.LED4_ON):
            self.ser.write('L4\r')
            self.led_on[3] = True
        if (cmd == self.DUTY_CYCLE):
            self.ser.write('D{0:d}\r'.format(int(self.cur_led_amp)))
        if (cmd == self.LED_OFF):
            self.ser.write('O\r')
            read_again = True
            for i in range(len(self.led_on)):
                self.led_on[i] = False
        if (cmd == self.RESET_5V):
            self.ser.write('RST\r')
        if (cmd == self.SERIAL_NUMBER):
            self.ser.write('SN\r')
        if (cmd == self.STATUS):
            self.ser.write('S\r')
        if (cmd == self.VERSION):
            self.ser.write('VER\r')
        if (cmd == self.ERROR_CHECK):
            self.ser.write('E\r')
        if (cmd == self.PRESSURE):
            self.ser.write('P\r')
        if (cmd == self.VACUUM_ON):
            self.ser.write('VAC1\r')
            self.vacuum_on = True
        if (cmd == self.VACUUM_OFF):
            self.ser.write('VAC0\r')
            self.vacuum_on = False
        if (cmd == self.VALVE_ON):
            self.ser.write('VAL1\r')
            self.valve_on = True
        if (cmd == self.VALVE_OFF):
            self.ser.write('VAL0\r')
            self.valve_on = False
        if (cmd == self.LCD1):
            self.ser.write('LCD1\r')
        if (cmd == self.LCD2):
            self.ser.write('LCD2\r')
        if (cmd == self.LCD3):
            self.ser.write('LCD3\r')
        if (cmd == self.LCD4):
            self.ser.write('LCD4\r')
        if (cmd == self.LCD5):
            self.ser.write('LCD5\r')
        if (cmd == self.LCD6):
            self.ser.write('LCD6\r')
        if (cmd == self.LCD7):
            self.ser.write('LCD7\r')

    def respond(self, cmd):
        #if (cmd == self.NOTHING):
        #    self.ser.write('\r')
        #if (cmd == self.LED1_ON):
        #    self.ser.write('L1\r')
        #    self.led_on[0] = True
        #if (cmd == self.LED2_ON):
        #    self.ser.write('L2\r')
        #    self.led_on[1] = True
        #if (cmd == self.LED3_ON):
        #    self.ser.write('L3\r')
        #    self.led_on[2] = True
        #if (cmd == self.LED4_ON):
        #    self.ser.write('L4\r')
        #    self.led_on[3] = True
        #if (cmd == self.DUTY_CYCLE):
        #    self.ser.write('D{0:d}\r'.format(int(self.cur_led_amp)))
        #if (cmd == self.LED_OFF):
        #    self.ser.write('O\r')
        #    read_again = True
        #    for i in range(len(self.led_on)):
        #        self.led_on[i] = False
        #if (cmd == self.RESET_5V):
        #    self.ser.write('RST\r')
        #if (cmd == self.SERIAL_NUMBER):
        #    self.ser.write('SN\r')
        #if (cmd == self.STATUS):
        #    self.ser.write('S\r')
        #if (cmd == self.VERSION):
        #    self.ser.write('VER\r')
        #if (cmd == self.ERROR_CHECK):
        #    self.ser.write('E\r')
        if (cmd == self.PRESSURE):
            self.pressure_measurement = self.interface
            
        ### SETTING THEM HERE (THIS IS THE CORRECT PLACE)
        ### BUT THEY ARE SET ABOVE BECAUSE WE HAVEN'T ADDED CLOSED LOOP FEEDBACK
        if (cmd == self.VACUUM_ON):
            self.vacuum_on = True #self.interface
        if (cmd == self.VACUUM_OFF):
            self.vacuum_on = False #self.interface
        if (cmd == self.VALVE_ON):
            self.valve_on = True #self.interface
        if (cmd == self.VALVE_OFF):
            self.valve_on = False #self.interface

    def command(self, cmd):
        self.success = False
        if (self.arduino_port != 'COM0'):
            try:
                #self.ser = serial.Serial(self.arduino_port, self.arduino_com_speed, timeout=1)
                self.ser.write('\r') #send dummy command, bug in Arduino when restarting
                self.interface = self.ser.readline().strip()
                self.command_issue(cmd)
                self.interface = self.ser.readline().strip()
                self.respond(cmd)
                #self.ser.close()
                self.success = True
            except:
                print "LED: Failed To Connect: " + self.arduino_port
                self.success = False
        return cmd
            
            
