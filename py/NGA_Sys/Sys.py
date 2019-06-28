'''
Created on Jan 24, 2014

@author: dfreedman
'''

from NGA_Interface.Interface import NGA_Interface

from NGA_Config.Window import NGA_Config_Window
from NGA_Config.Py import NGA_Config_Py

class NGA_Sys:
    
    hw = None
    win_cfg = None
    py_cfg = None

    def __init__(self):
        self.hw = NGA_Interface()
        self.win_cfg = NGA_Config_Window()
        self.py_cfg = NGA_Config_Py()
        
        # these windows add their hooks 
        # this seems like the easiest way to make callbacks
        
        #self.sys.c_cam #Camera Window
        #self.sys.c_config_window #Config Window
        #self.sys.c_led_advanced  #LED Advanced
        #self.sys.c_led #LED
        #self.sys.c_process #Process Window
        #self.sys.c_stage #Stage Window