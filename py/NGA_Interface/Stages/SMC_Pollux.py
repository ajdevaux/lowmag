import serial
from Virtual_Stage import Virtual_Stage

from NGA_Config.Stage_Ports import NGA_Config_Stage_Ports
from NGA_Utils.Stage_Status import NGA_Stage_Status

# NGA CLASSES

## this class only support the Z-axis
class SMC_Pollux(Virtual_Stage):

    name = "pollux"
    stage_config = None
    com_port = ""
    com_speed = 19200
    success = False
    loaded = False
    serial_out = ""
    serial_parse = ""
    
    x_axis = "1"
    y_axis = "3"
    z_axis = "2"
    
    def __init__(self):
        self.interface = self.STAGE_SMC_POLLUX
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
        if 'pollux' in self.stage_config.defaults.config:
            self.com_port = self.stage_config.defaults.config['pollux']
            if (self.com_port != 'COM0'):
                try:
                    #connect to serial port
                    self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.5)
                    print "Stage: Loaded: SMC POLLUX"
                    self.loaded = True
                except:
                    print "Stage: Not Loaded: SMC POLLUX: Failed Connection, port: " + self.com_port
            else:
                print "Stage: NOT Loaded: SMC POLLUX"
        else:
            self.com_port = 'COM0'
            print "Stage: NOT Loaded: SMC POLLUX"
            

    def stage_name(self):
        return self.name
            
    def move_rel_x(self, x_pos):
        self.x_pos = self.x_pos + x_pos
        send_command = "{0:.6f} {1} nr".format(x_pos,self.x_axis)
        self.ser_write(send_command)
        
    def move_rel_y(self, y_pos):
        self.y_pos = self.y_pos + y_pos
        send_command = "{0:.6f} {1} nr".format(y_pos,self.y_axis)
        self.ser_write(send_command)
    
    def move_rel_z(self, z_pos):
        self.z_pos = self.z_pos + z_pos
        send_command = "{0:.6f} {1} nr".format(z_pos,self.z_axis)
        self.ser_write(send_command)
        
    def move_x(self, x_pos):
        self.x_pos = x_pos
        send_command = "{0:.6f} {1} nm".format(self.x_pos,self.x_axis)
        self.ser_write(send_command)
        
    def move_y(self, y_pos):
        self.y_pos = y_pos
        send_command = "{0:.6f} {1} nm".format(self.y_pos,self.y_axis)
        self.ser_write(send_command)
    
    def move_z(self, z_pos):
        self.z_pos = z_pos
        send_command = "{0:.6f} {1} nm".format(self.z_pos,self.z_axis)
        self.ser_write(send_command)
        
    def move_serial_x_y_z(self, x_pos, y_pos, z_pos):
        self.move_x(x_pos)
        self.move_y(y_pos)
        self.move_z(z_pos)
    
    # TO DO      
    def move_parrallel_x_y_z(self, x_pos, y_pos, z_pos):
        self.move_x(x_pos)
        self.move_y(y_pos)
        self.move_z(z_pos)
    
    def get_actual_position(self):
        # this is the actual positions from the stage
        send_command = self.x_axis + " np"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            self.actual_x_pos = float(self.serial_parse)
        else:
            print "Stage: Location Command Failed"


        send_command = self.y_axis + " np"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            self.actual_y_pos = float(self.serial_parse)
        else:
            print "Stage: Location Command Failed"

            
        send_command = self.z_axis + " np"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            self.actual_z_pos = float(self.serial_parse)
        else:
            print "Stage: Location Command Failed"
        #if len(tmp) == 3: # if it included X, Y, Z
        #    self.actual_x_pos = self.mm(float(tmp[0]))
        #    self.actual_y_pos = self.mm(float(tmp[1]))
        #    self.actual_z_pos = self.mm(float(tmp[2]))
            
    def home(self):
        send_command = self.x_axis + " ncal;" + self.y_axis + " ncal;" + self.z_axis + " ncal;"
        #send_command = self.z_axis + " ncal"
        self.ser_write(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
        
    def zero(self):
        # do nothing here because ncal zeros for us
        #send_command = "3 ncal"
        #self.ser_write(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
    
    def abort(self):
        send_command = self.x_axis + " nabort;" + self.y_axis + " nabort;" + self.z_axis + " nabort;"
        self.ser_write(send_command)       
    
    ### DEBUGGED WITH Z STAGE
    def update_status(self, xyz_str):
        # xyz, can be anything, will return Z axis only
        stage_status = NGA_Stage_Status()
        self.status = stage_status.config
            
        if (xyz_str == 'x'):
            send_command = self.x_axis + " nstatus"
            self.ser_response(send_command)
            self.status['axis_enabled'] = True    
            if (len(self.serial_parse) > 0):
                byte = round(float(self.serial_parse))
                if (byte >= 128):
                    byte = byte - 128
                    # moto enable state
                if (byte >= 64):
                    byte = byte - 64
                    # motor driver state
                if (byte >= 32):
                    byte = byte - 32
                    self.status['closed_loop_in_window'] = True
                if (byte >= 16):
                    byte = byte - 16
                    # speed mode on/off
                if (byte >= 8):
                    byte = byte - 8
                    #self.status['joystick_enabled'] = True
                if (byte >= 4):
                    byte = byte - 4
                    self.status['motor_enabled'] = True
                if (byte >= 2):
                    byte = byte - 2
                    #self.status['axis_enabled'] = True
                if (byte >= 1):
                    byte = byte - 1
                    self.status['axis_moving'] = True
        if (xyz_str == 'y'):
            send_command = self.y_axis + " nstatus"
            self.ser_response(send_command)
            self.status['axis_enabled'] = True    
            if (len(self.serial_parse) > 0):
                byte = round(float(self.serial_parse))
                if (byte >= 128):
                    byte = byte - 128
                    # moto enable state
                if (byte >= 64):
                    byte = byte - 64
                    # motor driver state
                if (byte >= 32):
                    byte = byte - 32
                    self.status['closed_loop_in_window'] = True
                if (byte >= 16):
                    byte = byte - 16
                    # speed mode on/off
                if (byte >= 8):
                    byte = byte - 8
                    #self.status['joystick_enabled'] = True
                if (byte >= 4):
                    byte = byte - 4
                    self.status['motor_enabled'] = True
                if (byte >= 2):
                    byte = byte - 2
                    #self.status['axis_enabled'] = True
                if (byte >= 1):
                    byte = byte - 1
                    self.status['axis_moving'] = True
        if (xyz_str == 'z'):
            send_command = self.z_axis + " nstatus"
            self.ser_response(send_command)
            self.status['axis_enabled'] = True    
            if (len(self.serial_parse) > 0):
                byte = round(float(self.serial_parse))
                if (byte >= 128):
                    byte = byte - 128
                    # moto enable state
                if (byte >= 64):
                    byte = byte - 64
                    # motor driver state
                if (byte >= 32):
                    byte = byte - 32
                    self.status['closed_loop_in_window'] = True
                if (byte >= 16):
                    byte = byte - 16
                    # speed mode on/off
                if (byte >= 8):
                    byte = byte - 8
                    #self.status['joystick_enabled'] = True
                if (byte >= 4):
                    byte = byte - 4
                    self.status['motor_enabled'] = True
                if (byte >= 2):
                    byte = byte - 2
                    #self.status['axis_enabled'] = True
                if (byte >= 1):
                    byte = byte - 1
                    self.status['axis_moving'] = True
        
        return self.status
    
    
    # we'll use programs to define particle functions
    def program12(self):
        #send_command = "LOCK"
        send_command = "1 " + self.z_axis + " setcloop"
        self.ser_write(send_command)
  
    def program13(self):
        #send_command = "UNLOCK"
        send_command = "0 " + self.z_axis + " setcloop"
        self.ser_write(send_command)


    def ser_response(self, command):
        #print command
        self.success = False
        self.serial_parse = "" #clear this out in case of error        
        try: 
            #connect to serial port
            #self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.2)
            str_command = str(command) + '\r'
            self.ser.write(str_command) #send  command
            self.serial_out = self.ser.readline()
            #print "COM:" + command + ", " + self.serial_out
            #self.ser.close()
            self.check_response()
        except:
            print "Stage: Failed To Connect: SMC Pollux"

    def ser_write(self, command):
        #print command
        self.success = False
                
        try: 
            #connect to serial port
            #self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.01)
            str_command = str(command) + '\r'
            self.ser.write(str_command) #send  command
            #self.serial_out = self.ser.readline()
            #print "COM:" + command + ", " + self.serial_out
            #self.ser.close()
            #self.check_response()
            self.success = True
        except:
            print "Stage: Failed To Connect: SMC Pollux"

    def check_response(self):
        #print self.serial_out
        self.serial_parse = self.serial_out.strip() # get rid of random newlines and carriage returns
        self.success = True
      
