import serial
from Virtual_Stage import Virtual_Stage

from NGA_Config.Stage_Ports import NGA_Config_Stage_Ports
from NGA_Utils.Stage_Status import NGA_Stage_Status

import time

# NGA CLASSES

## this class only support the MFC-2000 (CRISP) in the Z-axis
# and the SMC Pollux in the X & Y directions 
class MFC_Pollux_Hybrid(Virtual_Stage):

    name = "mfc_pollux_hybrid"
    stage_config = None
    com_port_mfc = ""
    com_port_pollux = ""
    com_speed_mfc = 9600
    com_speed_pollux = 19200
    success = False
    loaded = False
    serial_out = ""
    serial_parse = ""
    
    x_axis = "1"
    y_axis = "3"
    z_axis = "Z"
    
    
    def __init__(self):
        self.interface = self.STAGE_MFC_POLLUX_HYBRID
        self._init() #load superclass vals
        self.load()
        
    def __del__(self):
        self.close()

    def close(self):
        if (self.loaded == True):
            self.loaded = False
            self.ser_mfc.close()
            self.ser_pollux.close()
    
    def load(self):
        self.serial_out = ""
        self.serial_parse = ""
        self.success = False
        self.loaded = False
        self.stage_config = NGA_Config_Stage_Ports()
        if 'mfc2000' in self.stage_config.defaults.config:
            self.com_port_mmc = self.stage_config.defaults.config['mfc2000']
            if (self.com_port_mmc != 'COM0'):
                try:
                    #connect to serial port
                    self.ser_mmc = serial.Serial(self.com_port_mfc, self.com_speed_mfc, timeout=0.5)
                    print "Stage: Loaded: MFC 2000"
                    self.loaded = True
                except:
                    print "Stage: Not Loaded: MFC 2000: Failed Connection, port: " + self.com_port_mfc
            else:
                print "Stage: NOT Loaded: MFC 2000: Not Found"
        else:
            self.com_port_mmc = 'COM0'
            print "Stage: NOT Loaded: MFC 2000:  Not Configured"
            
        if (self.loaded == True): #only proceed if all stages load
            self.loaded = False
            if 'pollux' in self.stage_config.defaults.config:
                self.com_port_pollux = self.stage_config.defaults.config['pollux']
                if (self.com_port_pollux != 'COM0'):
                    try:
                        #connect to serial port
                        self.ser_pollux = serial.Serial(self.com_port_pollux, self.com_speed_pollux, timeout=0.5)
                        print "Stage: Loaded: SMC POLLUX"
                        self.loaded = True
                    except:
                        print "Stage: Not Loaded: SMC POLLUX: Failed Connection, port: " + self.com_port_pollux
                else:
                    print "Stage: NOT Loaded: SMC POLLUX: Not Found"
            else:
                self.com_port_pollux = 'COM0'
                print "Stage: NOT Loaded: SMC POLLUX:  Not Configured"
            
    
    def stage_name(self):
        return self.name
    
    def tenths_of_microns(self, mm):
        return mm*10000.0
    def mm(self, tenths_of_microns):
        return tenths_of_microns/10000.0
      
    # from SMC_Pollux.py      
    def move_rel_x(self, x_pos):
        self.x_pos = self.x_pos + x_pos
        send_command = "{0:.6f} {1} nr".format(x_pos,self.x_axis)
        self.ser_pollux_write(send_command)
    # from SMC_Pollux.py    
    def move_rel_y(self, y_pos):
        self.y_pos = self.y_pos + y_pos
        send_command = "{0:.6f} {1} nr".format(y_pos,self.y_axis)
        self.ser_pollux_write(send_command)
    
    # from MFC_2000.py
    def move_rel_z(self, z_pos):
        self.z_pos = self.z_pos + z_pos
        pos_to_move = self.tenths_of_microns(self.z_pos)
        send_command = "MOVEREL Z={0:.2f}".format(pos_to_move)
        self.ser_mfc_response(send_command)

    
    # from SMC_Pollux.py     
    def move_x(self, x_pos):
        self.x_pos = x_pos
        send_command = "{0:.6f} {1} nm".format(self.x_pos,self.x_axis)
        self.ser_pollux_write(send_command)
    # from SMC_Pollux.py     
    def move_y(self, y_pos):
        self.y_pos = y_pos
        send_command = "{0:.6f} {1} nm".format(self.y_pos,self.y_axis)
        self.ser_pollux_write(send_command)
    
    # from MFC_2000.py
    def move_z(self, z_pos):
        self.z_pos = z_pos
        pos_to_move = self.tenths_of_microns(self.z_pos)
        send_command = "MOVE Z={0:.2f}".format(pos_to_move)
        self.ser_mfc_response(send_command)
        
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
        
        # from SMC_Pollux.py
        send_command = self.x_axis + " np"
        self.ser_pollux_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            self.actual_x_pos = float(self.serial_parse)
        else:
            print "Stage: Location Command Failed"
            
        send_command = self.y_axis + " np"
        self.ser_pollux_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            self.actual_y_pos = float(self.serial_parse)
        else:
            print "Stage: Location Command Failed"
        
        # from MFC_2000.py
        send_command = "WHERE Z"
        self.ser_mfc_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            tmp = self.serial_parse.split(" ")
            if len(tmp) == 1: # only Z
                self.actual_z_pos = self.mm(float(tmp[0]))
            else:
                print "Stage: Location Command Failed"
        
    def home(self):
        # from MFC_2000.py
        send_command = "HOME Z"
        self.ser_mfc_response(send_command)
        
        # from SMC_Pollux.py
        send_command = self.x_axis + " ncal;" + self.y_axis + " ncal;"
        self.ser_pollux_write(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        
    def zero(self):
        
        # from MFC_2000.py
        send_command = "Z"
        self.ser_mfc_response(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0
    
    def abort(self):
        
        # from MFC_2000.py
        send_command = self.z_axis + " HALT"
        self.ser_mfc_response(send_command)
        
        # from SMC_Pollux.py
        send_command = self.x_axis + " nabort;" + self.y_axis + " nabort;"
        self.ser_pollux_write(send_command)  
    
    ### DEBUGGED WITH Z STAGE
    def update_status(self, xyz_str):
        # xyz, can be anything, will return Z axis only
        stage_status = NGA_Stage_Status()
        self.status = stage_status.config
            
        # from SMC_Pollux.py    
        if (xyz_str == 'x'):
            send_command = self.x_axis + " nstatus"
            self.ser_pollux_response(send_command)
            
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
            self.ser_pollux_response(send_command)
            
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
                       
        # from MFC_2000.py
        if (xyz_str == 'z'):
            send_command = "RDSBYTE Z"
            self.ser_mfc_response(send_command)        
        
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

    def program12(self): #enable closed loop
        
        # from MFC_2000.py
        send_command = "LOCK"
        self.ser_mfc_write(send_command)
        
        # from SMC_Pollux.py
        send_command = "1 " + self.x_axis + " setcloop"
        self.ser_pollux_write(send_command)
        
        send_command = "1 " + self.y_axis + " setcloop"
        self.ser_pollux_write(send_command)
  
  
    def program13(self): #turn off closed loop
        
        # from MFC_2000.py
        send_command = "UNLOCK"
        self.ser_mfc_write(send_command)
        
        # from SMC_Pollux.py
        send_command = "0 " + self.x_axis + " setcloop"
        self.ser_pollux_write(send_command)
        
        send_command = "0 " + self.y_axis + " setcloop"
        self.ser_pollux_write(send_command)

    def ser_pollux_response(self, command):
        self.success = False
        self.serial_parse = "" #clear this out in case of error        
        try: 
            str_command = str(command) + '\r'
            self.ser_pollux.write(str_command) #send  command
            self.serial_out = self.ser_pollux.readline()
            self.check_pollux_response()
        except:
            print "Stage: Failed To Connect: SMC POLLUX"

    def ser_pollux_write(self, command):
        self.success = False          
        try: 
            str_command = str(command) + '\r'
            self.ser_pollux.write(str_command) #send  command
            self.success = True
        except:
            print "Stage: Failed To Connect: SMC POLLUX"
            
    def ser_mfc_response(self, command):
        self.success = False
        self.serial_parse = "" #clear this out in case of error        
        try: 
            str_command = str(command) + '\r'
            self.ser_mfc.write(str_command) #send  command
            self.serial_out = self.ser_mfc.readline()
            self.check_mmc_response()
        except:
            print "Stage: Failed To Connect: MFC 2000"

    def ser_mfc_write(self, command):
        self.success = False    
        try: 
            str_command = str(command) + '\r'
            self.ser_mfc.write(str_command) #send  command
            self.success = True
        except:
            print "Stage: Failed To Connect: MFC 2000"

    def check_mfc_response(self):
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

            
    def check_pollux_response(self):
        self.serial_parse = self.serial_out.strip() # get rid of random newlines and carriage returns
        self.success = True


        
