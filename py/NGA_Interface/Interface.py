'''
This class is the global hardware control. All sub-interfaces are instantiated in his class.
Created on Jan 24, 2014

@author: dfreedman
'''

from Camera import NGA_Interface_Camera
from LED import NGA_Interface_LED
from Network import NGA_Interface_Network
from Stage import NGA_Interface_Stage

class NGA_Interface:

    cam = None
    led = None
    net = None
    stg = None
    
    def __init__(self):
        self.reload()
        
    def reload(self):
        #self.reload_cam()
        self.reload_led()
        #self.reload_net()
        #self.reload_stage()
        
    #def reload_cam(self):
        #self.cam = NGA_Interface_Camera()
        
    def reload_led(self):
        self.clear_led()
        self.led = NGA_Interface_LED()
        
    def reload_net(self):
        self.net = NGA_Interface_Network()
        
    def clear_stage(self):
        #when searching for ports, we should make sure to close the stage serial port
        self.stg = None
        
    def clear_led(self):
        #when searching for ports, we should make sure to close the led serial port
        self.led = None
        
    def reload_stage(self):
        self.clear_stage()
        self.stg = NGA_Interface_Stage()
