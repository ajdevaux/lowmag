import serial
from Virtual_Stage import Virtual_Stage

from NGA_Config.Stage_Ports import NGA_Config_Stage_Ports
from NGA_Utils.Stage_Status import NGA_Stage_Status

# NGA CLASSES

## this class only support the Z-axis
class MFC_2000(Virtual_Stage):

    name = "mfc2000"
    stage_config = None
    com_port = ""
    com_speed = 9600
    success = False
    loaded = False
    serial_out = ""
    serial_parse = ""

    
    def __init__(self):
        self.interface = self.STAGE_MFC2000
        self._init() #load superclass vals
        self.load()

    def __del__(self):
        self.close()

    def close(self):
        if (self.loaded == True):
            self.loaded = False
            self.ser.close()

    def load(self):
        self.serial_out = ""
        self.serial_parse = ""
        self.success = False
        self.loaded = False
        self.stage_config = NGA_Config_Stage_Ports()
        if 'mfc2000' in self.stage_config.defaults.config:
            self.com_port = self.stage_config.defaults.config['mfc2000']
            if (self.com_port != 'COM0'):
                try:
                    #connect to serial port
                    self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.5)
                    print "Stage: Loaded: MFC 2000"
                    self.loaded = True
                except:
                    print "Stage: Not Loaded: MFC 2000: Failed Connection, port: " + self.com_port
            else:
                print "Stage: NOT Loaded: MFC 2000"
        else:
            self.com_port = 'COM0'
            print "Stage: NOT Loaded: MFC 2000"
            
            
    def tenths_of_microns(self, mm):
        return mm*10000.0
    def mm(self, tenths_of_microns):
        return tenths_of_microns/10000.0
    
    def stage_name(self):
        return self.name
            
    def move_rel_x(self, x_pos):
        self.x_pos = self.x_pos + x_pos
        pos_to_move = self.tenths_of_microns(self.x_pos)
        send_command = "MOVEREL X={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
        
    def move_rel_y(self, y_pos):
        self.y_pos = self.y_pos + y_pos
        pos_to_move = self.tenths_of_microns(self.y_pos)
        send_command = "MOVEREL Y={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
    
    def move_rel_z(self, z_pos):
        self.z_pos = self.z_pos + z_pos
        pos_to_move = self.tenths_of_microns(self.z_pos)
        send_command = "MOVEREL Z={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
        
    def move_x(self, x_pos):
        self.x_pos = x_pos
        pos_to_move = self.tenths_of_microns(self.x_pos)
        send_command = "MOVE X={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
        
    def move_y(self, y_pos):
        self.y_pos = y_pos
        pos_to_move = self.tenths_of_microns(self.y_pos)
        send_command = "MOVE Y={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
    
    def move_z(self, z_pos):
        self.z_pos = z_pos
        pos_to_move = self.tenths_of_microns(self.z_pos)
        send_command = "MOVE Z={0:.2f}".format(pos_to_move)
        self.ser_write(send_command)
        
    def move_serial_x_y_z(self, x_pos, y_pos, z_pos):
        self.move_x(x_pos)
        self.move_y(y_pos)
        self.move_z(z_pos)
         
    def move_parrallel_x_y_z(self, x_pos, y_pos, z_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        pos_to_move_x = self.tenths_of_microns(self.x_pos)
        pos_to_move_y = self.tenths_of_microns(self.y_pos)
        pos_to_move_z = self.tenths_of_microns(self.z_pos)
        #send_command = "MOVE X={0:.2f} Y={0:.2f} Z={0:.2f}".format(pos_to_move_x,pos_to_move_y,pos_to_move_z)
        send_command = "MOVE Z={0:.2f}".format(pos_to_move_z)
        self.ser_write(send_command)
    
    def get_actual_position(self):
        # this is the actual positions from the stage
        send_command = "WHERE Z"
        self.ser_write(send_command)
        print self.serial_parse
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            tmp = self.serial_parse.split(" ")
            if len(tmp) == 1: # only Z
                self.actual_z_pos = self.mm(float(tmp[0]))
            else:
                print "Stage: Location Command Failed"
        #if len(tmp) == 3: # if it included X, Y, Z
        #    self.actual_x_pos = self.mm(float(tmp[0]))
        #    self.actual_y_pos = self.mm(float(tmp[1]))
        #    self.actual_z_pos = self.mm(float(tmp[2]))
            
    def home(self):
        send_command = "HOME Z"
        self.ser_write(send_command)
        
    def zero(self):
        send_command = "Z"
        self.ser_write(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
    
    def abort(self):
        send_command = "HALT"
        self.ser_write(send_command)
    
    ### DEBUGGED WITH Z STAGE
    def update_status(self, xyz_str):
        stage_status = NGA_Stage_Status()
        self.status = stage_status.config
        # xyz, can be anything, will return Z axis only
        if (xyz_str == 'z'):
            send_command = "RDSBYTE Z"
            self.ser_write(send_command)        
        
            #self.status['axis_enabled'] = True    
            if (len(self.serial_out) > 1):
                byte = ord(self.serial_out[1:2])
        
                if (byte >= 128):
                    byte = byte - 128
                    self.status['lower_limit_swtich_closed'] = True
                if (byte >= 64):
                    byte = byte - 64
                    self.status['upper_limit_swtich_closed'] = True
                if (byte >= 32):
                    byte = byte - 32
                    self.status['motor_ramping_down'] = True
                if (byte >= 16):
                    byte = byte - 16
                    self.status['motor_ramping_up'] = True
                if (byte >= 8):
                    byte = byte - 8
                    self.status['joystick_enabled'] = True
                if (byte >= 4):
                    byte = byte - 4
                    self.status['motor_enabled'] = True
                if (byte >= 2):
                    byte = byte - 2
                    self.status['axis_enabled'] = True
                if (byte >= 1):
                    byte = byte - 1
                    self.status['axis_moving'] = True
            
        return self.status
    

    ## mm/s
    def hi_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = 3.00
        elif (xyz_str == 'y'):
            self.y_speed = 3.00
        elif (xyz_str == 'z'):
            self.z_speed = 0.5
        self.update_speed()
    def med_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = 0.5
        elif (xyz_str == 'y'):
            self.y_speed = 0.5
        elif (xyz_str == 'z'):
            self.z_speed = 0.1
        self.update_speed()
    def slow_speed(self, xyz_str):
        if (xyz_str == 'x'):
            self.x_speed = 0.1
        elif (xyz_str == 'y'):
            self.y_speed = 0.1
        elif (xyz_str == 'z'):
            self.z_speed = 0.02
        self.update_speed()
         
    def update_speed(self):
        #send_command = "SPEED X={0:.2f} Y={0:.2f} Z={0:.2f}".format(self.x_speed,self.y_speed,self.z_speed)
        send_command = "SPEED Z={0:.2f}".format(self.z_speed)
        self.ser_write(send_command)   
    
    
    # we'll use programs to define particle functions
    def program12(self):
        send_command = "LOCK"
        self.ser_write(send_command)
  
    def program13(self):
        send_command = "UNLOCK"
        self.ser_write(send_command)

   

    def ser_write_test(self, command):
        self.success = False
        #self.serial_out = ":A\r\n".strip()
        #self.serial_out = ":A X=1000.000\r\n".strip()
        self.serial_out = ":A 1.23\r\n"
        self.check_response()

    def ser_write(self, command):
        #print command
        self.serial_parse = "" #clear in case of error
        self.success = False
        try:
            #ser = serial.Serial(self.com_port, self.com_speed, timeout=1)
            str_command = str(command) + '\r'
            self.ser.write(str_command) #send dummy command
            self.serial_out = self.ser.readline()
            print self.serial_out
            #ser.close()
            self.check_response()
        except:
            print "Stage: Failed To Connect: MFC 2000"


    def check_response(self):
        #print "SERIAL: ", self.serial_out
        if (self.serial_out[0:2] == ":A"):
            if len(self.serial_out) > 2:
                self.serial_parse = self.serial_out[2:-1].strip()
            else:
                self.serial_parse = ""
            self.success = True
        else:
            self.serial_parse = ""
            self.success = False
