from Tkinter import Tk, Label, BOTH, Toplevel
from ttk import Frame, Button, Style

from NGA_Interface.LED import NGA_Interface_LED

class NGA_Window_Pneumatics(Frame):

    cfg = None
    
    sys = None
    vacuum_enabled = False
    valve_enabled = False
    pressure_val = 0

  
    def __init__(self, parent, sys):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.sys = sys
        # attach handle to this window class to main sys class
        self.sys.c_pneumatics = self

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wPneumatics)
        self.parent.title(self.sys.win_cfg.sPneumatics)

        # draw window
        self.initUI()

        # window defaults
        self.vacuum_enabled = False
        self.valve_enabled = False
        self.pressure_val = 0
        
    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        # setup labels
        self.Vacuum = Label(self, width=16, background=self.sys.win_cfg.cLEDOff, text="Idle")
        self.Vacuum.place(x=20, y=10)
        
        #duty cycle
        
        
        # setup buttons
        vacuumButton = Button(self, text="Toggle Vacuum",
            command=self.vacuum_toggle, width=15)
        vacuumButton.place(x=30, y=40)
        valveutton = Button(self, text="Toggle Valve",
            command=self.valve_toggle, width=15)
        valveutton.place(x=30, y=70)
        pressureButton = Button(self, text="Measure Pressure",
            command=self.measure_pressure, width=15)
        pressureButton.place(x=30, y=100)

        self.statusLabel = Label(self, width=15,
                                    background=self.sys.win_cfg.cBackground,
                                    text="")
        self.statusLabel.place(x=15, y=130)

        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=15)
        closeButton.place(x=30, y=160)

    
    def close_window(self):
        self.parent.destroy()
        
    def vacuum_toggle(self):
        if (self.vacuum_enabled == True):
            command = self.sys.hw.led.command(NGA_Interface_LED.VACUUM_OFF)
        if (self.vacuum_enabled == False):
            command = self.sys.hw.led.command(NGA_Interface_LED.VACUUM_ON)
        if (self.sys.hw.led.success == True):
            self.update_vacuum_on_off()
        else:
            self.pneumatics_status_error()
            return command
            
    def valve_toggle(self):
        if (self.valve_enabled == True):
            command = self.sys.hw.led.command(NGA_Interface_LED.VALVE_OFF)
        if (self.valve_enabled == False):
            command = self.sys.hw.led.command(NGA_Interface_LED.VALVE_ON)
        if (self.sys.hw.led.success == True):
            self.update_vacuum_on_off()
        else:
            self.pneumatics_status_error()
            return command
            
    def measure_pressure(self):
        self.sys.hw.led.command(NGA_Interface_LED.PRESSURE)
        tmp = self.sys.hw.led.interface
        self.pressure_val = self.convert_to_atm(tmp)
        self.pneumatics_status("Pressure: {0:.2f} PSI".format(self.pressure_val))
        return self.pressure_val
        
    def convert_to_atm(self, val):
        digital_value = 0
        if ":Pressure: " in val:
            tmp = val.split(":")
            ttnum = 0
            digital_value = 4096 #12-bit number
            for entry in tmp:
                word = entry.strip()
                ttnum = ttnum + 1
                if (ttnum == 3): #our value is on the third split
                    digital_value = word
            
            ratio_value = (float(digital_value)-166)/134 #max v = 4.7, min v = 0.2, fs = 4.5 V over 1024, 10-bit range
            digital_value = -1.0*ratio_value # 0-1 atm = 4.5 V scale
            # output is in ATM (as a ratio to sealevel atm)
            
        return digital_value
                            
    def pneumatics_status_error(self):
        self.pneumatics_status("ERROR")
    def pneumatics_status(self, msg):
        self.statusLabel.configure(text = msg)
        
    def update_vacuum_on_off(self):
        if self.sys.hw.led.vacuum_on == True: # PUMPING
            self.vacuum_enabled = True
            if self.sys.hw.led.valve_on == True: #WHILE CHIP IS CONNECTED? NO!
                self.valve_enabled = True
                self.Vacuum.configure(background = self.sys.win_cfg.cBad) #red, bad
                self.Vacuum.configure(text = "! Pumping with Chip")
            else:
                self.valve_enabled = False # Pumping down resevior
                self.Vacuum.configure(background = self.sys.win_cfg.cLEDOn2) 
                self.Vacuum.configure(text = "Pumping Reservoir")
        if self.sys.hw.led.vacuum_on == False: # Not Pumping
            
            self.vacuum_enabled = False
            if self.sys.hw.led.valve_on == True: # but connected o the chip
                self.valve_enabled = True
                self.Vacuum.configure(background = self.sys.win_cfg.cLEDOn)
                self.Vacuum.configure(text = "Chip Engaged")
            else: #Idle
                self.valve_enabled = False
                self.Vacuum.configure(background = self.sys.win_cfg.cUnknown)   
                self.Vacuum.configure(text = "Idle")
                                  
  
