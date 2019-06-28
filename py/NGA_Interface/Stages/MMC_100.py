import serial
from Virtual_Stage import Virtual_Stage

from NGA_Config.Stage_Ports import NGA_Config_Stage_Ports
from NGA_Utils.Stage_Status import NGA_Stage_Status

import time
import io

# NGA CLASSES

## this class only support the Z-axis
class MMC_100(Virtual_Stage):

    name = "mmc100"
    stage_config = None
    com_port = ""
    com_speed = 38400
    success = False
    loaded = False
    serial_out = ""
    serial_parse = ""
    
    x_axis = "2"
    y_axis = "3"
    z_axis = "1"
    
    
    def __init__(self):
        self.interface = self.STAGE_MMC100
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
        if 'mmc100' in self.stage_config.defaults.config:
            self.com_port = self.stage_config.defaults.config['mmc100']
            if (self.com_port != 'COM0'):
                try:
                    #connect to serial port
                    self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.5)
                    self.ser_io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1),  
                               newline = '\r',
                               line_buffering = True)
                    print "Stage: Loaded: MMC100"
                    self.loaded = True
                except:
                    print "Stage: Not Loaded: MMC100: Failed Connection, port: " + self.com_port
            else:
                print "Stage: NOT Loaded: MMC100: Not Found"
        else:
            self.com_port = 'COM0'
            print "Stage: NOT Loaded: MMC100:  Not Configured"
            
    
    def stage_name(self):
        return self.name
            
    def move_rel_x(self, x_pos):
        self.x_pos = self.x_pos + x_pos
        send_command = self.x_axis + " MVR " + "{0:.6f}".format(x_pos)
        self.ser_write(send_command)
        
    def move_rel_y(self, y_pos):
        self.y_pos = self.y_pos + y_pos
        send_command = self.y_axis + " MVR " + "{0:.6f}".format(y_pos)
        self.ser_write(send_command)
    
    def move_rel_z(self, z_pos):
        self.z_pos = self.z_pos + z_pos
        send_command = self.z_axis + " MVR " + "{0:.6f}".format(z_pos)
        self.ser_write(send_command)
        
    def move_x(self, x_pos):
        self.x_pos = x_pos
        send_command = self.x_axis + " MVA " + "{0:.6f}".format(self.x_pos)
        self.ser_write(send_command)
        return send_command
 
    def move_y(self, y_pos):
        self.y_pos = y_pos
        send_command = self.y_axis + " MVA " + "{0:.6f}".format(self.y_pos)
        self.ser_write(send_command)
        return send_command
    
    def move_z(self, z_pos):
        self.z_pos = z_pos
        send_command = self.z_axis + " MVA " + "{0:.6f}".format(self.z_pos)
        self.ser_write(send_command)
        return send_command
        
    def move_serial_x_y_z(self, x_pos, y_pos, z_pos):
        self.move_x(x_pos)
        self.move_y(y_pos)
        self.move_z(z_pos)
         
    def move_parrallel_x_y_z(self, x_pos, y_pos, z_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        sync_move = self.x_axis + " MSA " + "{0:.6f}".format(self.x_pos) +  ";"
        sync_move += self.y_axis + " MSA " + "{0:.6f}".format(self.y_pos) +  ";"
        sync_move += self.z_axis + " MSA " + "{0:.6f}".format(self.z_pos) +  ";"
        self.ser_write(sync_move)
        
        send_command = "0 RUN"
        self.ser_write(send_command)
    
    def get_actual_position(self):
        # this is the actual positions from the stage
        
        send_command = self.x_axis + " POS?"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            pos = self.parse_encoded_position(self.serial_parse)
            self.actual_x_pos = float(pos)
        else:
            print "Stage: Location Command Failed"
       
        send_command = self.y_axis + " POS?"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            pos = self.parse_encoded_position(self.serial_parse)
            self.actual_y_pos = float(pos)
        else:
            print "Stage: Location Command Failed"
          
        send_command = self.z_axis + " POS?"
        self.ser_response(send_command)
        # if stage is connected, otherwise we freak out here
        if len(self.serial_parse) > 0:
            pos = self.parse_encoded_position(self.serial_parse)
            self.actual_z_pos = float(pos)
        else:
            print "Stage: Location Command Failed"
        
    def home(self):
        ## Z has problem and will home incorrectly if not above Zero mark, so move to top and home again
        send_command = self.z_axis + " HOM"
        self.ser_write(send_command)
        zstatus = self.update_status('z')
        while ( (zstatus['axis_moving'] == True) ):
            zstatus = self.update_status('z')
            time.sleep(0.05)
        
        send_command = self.x_axis + " HOM"
        self.ser_write(send_command)
        send_command = self.y_axis + " HOM"
        self.ser_write(send_command)

        
        #send_command = self.z_axis + " HOM"
        #self.ser_write(send_command)
        
    def zero(self):
        send_command = self.x_axis + " ZRO"
        self.ser_write(send_command)
        send_command = self.y_axis + " ZRO"
        self.ser_write(send_command)
        send_command = self.z_axis + " ZRO"
        self.ser_write(send_command)
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.z_pos = 0.0

    
    def abort(self):
        send_command = self.z_axis + " EST"
        self.ser_write(send_command)
        send_command = self.y_axis + " EST"
        self.ser_write(send_command)
        send_command = self.x_axis + " EST"
        self.ser_write(send_command)
    
    ### DEBUGGED WITH Z STAGE
    def update_status(self, xyz_str):
        # xyz, can be anything, will return Z axis only
        stage_status = NGA_Stage_Status()
        self.status = stage_status.config
            
            
        if (xyz_str == 'x'):
            send_command = self.x_axis + " STA?"
            self.ser_response(send_command)  
            
        if (xyz_str == 'y'):
            send_command = self.y_axis + " STA?"
            self.ser_response(send_command)   
                
        if (xyz_str == 'z'):
            send_command = self.z_axis + " STA?"
            self.ser_response(send_command)
            
        self.status['axis_enabled'] = True  
        
        if (len(self.serial_parse) > 1):
            byte = int(self.serial_parse)
            #print byte
            if (byte >= 128): # 1>= errors have occurred. Use ERR? Or CER to clear
                byte = byte - 128
                self.status['error'] = True
            if (byte >= 64): # Currently in Acceleration phase of motion
                byte = byte - 64
                self.status['acceleration'] = True  
            if (byte >= 32): # Currently in Constant Velocity phase of motion
                byte = byte - 32
                self.status['constant_velocity'] = True 
            if (byte >= 16): # Currently in Deceleration phase of motion
                byte = byte - 16
                self.status['deceleration'] = True 
            if (byte >= 8): #Stage has stopped. (In Closed Loop Stage, is in the deadband)
                byte = byte - 8
                self.status['axis_moving'] = False 
            else:
                self.status['axis_moving'] = True
            if (byte >= 4): #A Program is currently running
                byte = byte - 4
                self.status['program_running'] = True 
            if (byte >= 2): #Positive Switch is Activated
                byte = byte - 2
                self.status['upper_limit_swtich_closed'] = True
            if (byte >= 1): #Negative Switch is Activated
                byte = byte - 1
                self.status['lower_limit_swtich_closed'] = True
        
        return self.status

    def program12(self):
        #send_command = "LOCK"
        send_command = self.x_axis + " FBK 3"
        self.ser_write(send_command)
        send_command = self.y_axis + " FBK 3"
        self.ser_write(send_command)
        send_command = self.z_axis + " FBK 3"
        self.ser_write(send_command)
  
    def program13(self):
        #send_command = "UNLOCK"
        send_command = self.x_axis + " FBK 0"
        self.ser_write(send_command)
        send_command = self.y_axis + " FBK 0"
        self.ser_write(send_command)
        send_command = self.z_axis + " FBK 0"
        self.ser_write(send_command)

    def ser_response(self, command):
        #print command
        self.success = False
        self.serial_parse = "" #clear this out in case of error        
        try: 
            #connect to serial port
            #self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.2)
            str_command = str(command) + '\r'
            self.ser_io.write(unicode(str_command)) #send  command
            #print "inwaiting %d" % self.ser.inWaiting()
            self.serial_out = self.ser_io.readline()
            #print "COM:" + command + ", " + self.serial_out
            #self.ser.close()
            self.check_response()
        except:
            print "Stage: Failed To Connect: MMC100 this"

    def ser_write(self, command):
        #print command
        self.success = False
                
        try: 
            #connect to serial port
            #self.ser = serial.Serial(self.com_port, self.com_speed, timeout=0.01)
            str_command = str(command) + '\r'
            self.ser_io.write(unicode(str_command)) #send  command
            #self.serial_out = self.ser.readline()
            #print "COM:" + command + ", " + self.serial_out
            #self.ser.close()
            #self.check_response()
            self.success = True
        except:
            print "Stage: Failed To Connect: MMC100"

    def check_err(self,axis):
        #self.ser_response("3 ERR?")
        str_command = str(axis) + "ERR?\r"
        self.ser_io.write(unicode(str_command)) #send  command
        res = self.ser_io.readline()
        print res
        if (len(res) < 5):
            print "no error %d" % len(res)
            return 0
        else:
            print "error %d" % len(res)
            return res

    def check_response(self):
        self.serial_parse = self.serial_out.strip() # get rid of random newlines and carriage returns
        if (self.serial_parse[0] == "#"): #pound means OK
            self.serial_parse = self.serial_parse.replace("#", "") # remove the first character
            self.success = True
        else:
            self.serial_parse = ""
            self.success = False


    def parse_encoded_position(self, pos_reponse):
        try:
            if (pos_reponse.count(",") > 0):
                tmp = pos_reponse.split(",")
                #print tmp[1]
                return tmp[1]
        except:
            #print "Closed loop off:"
            #print newstr
            return pos_reponse
                
    def parse_position(self,pos_reponse):
        if (pos_reponse.count(",") > 0):
            tmp = pos_reponse.split(",")
        #print tmp[0]
        return tmp[0]
        
