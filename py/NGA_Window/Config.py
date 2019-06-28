from Tkinter import Label, BOTH
from ttk import Frame, Button, Style

# NGA CLASS IMPORT
from NGA_Config.Serial_Scan import NGA_Config_Serial_Scan

class NGA_Window_Config(Frame):

    com = None
    sys = None

    

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)  
        
        self.sys = sys
        self.sys.c_config_window = self

        self.parent = parent

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wConfig)
        self.parent.title(self.sys.win_cfg.sConfig)

        # draw window
        self.initUI()

        # window defaults
                

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        # setup labels
        self.Embedded = Label(self, width=15,
                             background=self.sys.win_cfg.cUnknown, text="LED: COM0")
        self.Embedded.place(x=15, y=35)
        self.Stage = Label(self, width=15,
                            background=self.sys.win_cfg.cUnknown, text="Stages: COM0")
        self.Stage.place(x=15, y=60)

        # setup buttons
        configComButton = Button(self, text="COM Port Setup",
            command=self.com_port_search, width=17)
        configComButton.place(x=15, y=5)
        

        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=17)
        closeButton.place(x=15, y=90)

    def close_window(self):
        self.parent.destroy()
    
    def com_port_search(self):
        self.Embedded.configure(text = "LED: Searching ...")
        self.Stage.configure(text = "Stages: Searching ...")
        
        # close stages because we are going to look at all ports
        self.sys.hw.clear_stage()
        self.sys.hw.clear_led()
        
        self.Embedded.configure(background = self.sys.win_cfg.cBad)
        self.Stage.configure(background = self.sys.win_cfg.cBad)
        self.parent.update()
        self.com = NGA_Config_Serial_Scan()
        self.update_connections()

    def update_connections(self):
        self.Embedded.configure(text = "LED: " + self.com.serial_arduino)
        if (self.com.serial_arduino != "COM0"):
            self.Embedded.configure(background = self.sys.win_cfg.cGood)
        else:
            self.Stage.configure(text = "LED: NOT FOUND")
            self.Embedded.configure(background = self.sys.win_cfg.cBad)
            
        if self.com.stage == "mmc100": 
            self.Stage.configure(text = "Stages: MMC: " + self.com.serial_MMC100)
            self.Stage.configure(background = self.sys.win_cfg.cGood)
        elif self.com.stage == "mfc2000": 
            self.Stage.configure(text = "Stages: MFC: " + self.com.serial_MFC2000)
            self.Stage.configure(background = self.sys.win_cfg.cGood)
        elif self.com.stage == "smc-pollux": 
            self.Stage.configure(text = "Stages: SMC: " + self.com.serial_SMCPOLLUX)
            self.Stage.configure(background = self.sys.win_cfg.cGood)
        elif self.com.stage == "mmc_pollux_hybrid": 
            self.Stage.configure(text = self.com.serial_MMC100 + "/" + self.com.serial_SMCPOLLUX)
            self.Stage.configure(background = self.sys.win_cfg.cGood)
        elif self.com.stage == "mfc_pollux_hybrid": 
            self.Stage.configure(text = self.com.serial_MFC2000 + "/" + self.com.serial_SMCPOLLUX)
            self.Stage.configure(background = self.sys.win_cfg.cGood)
        else:
            self.Stage.configure(text = "Stages: NOT FOUND")
            self.Stage.configure(background = self.sys.win_cfg.cBad)
            
        # reload stages because port may have changed
        self.sys.c_main_window.reload_leds()
        self.sys.c_main_window.reload_stages()
