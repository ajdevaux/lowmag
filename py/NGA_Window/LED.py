from Tkinter import Tk, Label, BOTH, Toplevel
from ttk import Frame, Button, Style

from NGA_Interface.LED import NGA_Interface_LED

from LED_Advanced import NGA_Window_LED_Advanced

class NGA_Window_LED(Frame):

    cfg = None
    c_LEDAdv = None
    w_LEDAdv = None
    
    sn = ""
    status = ""
    sys = None

  
    def __init__(self, parent, sys):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.sys = sys
        # attach handle to this window class to main sys class
        self.sys.c_led = self
        
        self.sn = ""
        self.status = ""
        
        self.sys.hw.reload_led()

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wLED)
        self.parent.title(self.sys.win_cfg.sLED)

        # draw window
        self.initUI()

        # window defaults
        self.led_off()
        
         # LED Advanced Panel
        self.w_LEDAdv = Toplevel(self.parent)
        self.c_LEDAdv = NGA_Window_LED_Advanced(self.w_LEDAdv, self.sys)
        self.c_LEDAdv.close_window()

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        # setup labels
        self.LED1 = Label(self, width=10, background=self.sys.win_cfg.cLEDOff, text="LED1")
        self.LED1.place(x=30, y=10)
        
        #duty cycle
        
        
        # setup buttons
        ledonButton = Button(self, text="LED On",
            command=self.led_on)
        ledonButton.place(x=30, y=40)
        ledoffButton = Button(self, text="LED Off",
            command=self.led_off)
        ledoffButton.place(x=30, y=70)
        serialButton = Button(self, text="Serial",
            command=self.led_serial_status)
        serialButton.place(x=30, y=100)
        #ledstatusButton = Button(self, text="Status",
        #    command=self.led_status)
        #ledstatusButton.place(x=30, y=130)
        ledAdvButton = Button(self, text="Advanced",
            command=self.led_advanced)
        ledAdvButton.place(x=30, y=130)
        self.ledstatusLabel = Label(self, width=15,
                                    background=self.sys.win_cfg.cBackground,
                                    text="LED: Status: X")
        self.ledstatusLabel.place(x=15, y=158)

        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window)
        closeButton.place(x=30, y=180)

    
        
    def update_led(self):
        self.update_led_on_off()

    def update_advanced_led(self):
        try:
            if (self.c_LEDAdv.winfo_exists() == 1): #window exists
                self.c_LEDAdv.update_led()
        except:
            pass #this will error out if window hasn't loaded yet, that's ok
        
    def close_window(self):
        self.parent.destroy()
    def led_on(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        self.sys.hw.led.duty_cycle(0,255)
        if (self.sys.hw.led.success == True):
            self.update_led_on_off()
        else:
            self.led_status_error()
    def led_off(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        if (self.sys.hw.led.success == True):
            self.update_led_on_off()
        else:
            self.led_status_error()
    def led_status(self):
        self.sys.hw.led.command(NGA_Interface_LED.STATUS)
        self.status = self.sys.hw.led.interface
        self.ledstatusLabel.configure(text = "LED: Status: " + self.status)
    def led_serial(self):
        self.sys.hw.led.command(NGA_Interface_LED.STATUS)
        self.sn = self.sys.hw.led.interface
        self.ledstatusLabel.configure(text = "LED: SN: " + self.sn)
    def led_serial_status(self):
        self.sys.hw.led.command(NGA_Interface_LED.SERIAL_NUMBER)
        self.sn = self.sys.hw.led.interface
        self.sys.hw.led.command(NGA_Interface_LED.STATUS)
        self.status = self.sys.hw.led.interface
        msg = "LED: SN: " + self.sn + ", " + self.status
        self.ledstatusLabel.configure(text = msg)
    def led_status_error(self):
        msg = "ERROR"
        self.ledstatusLabel.configure(text = msg)
    def update_led_on_off(self):
        if self.sys.hw.led.led_on[0] == True:
            self.LED1.configure(background = self.sys.win_cfg.cLEDOn)
        if self.sys.hw.led.led_on[0] == False:
            self.LED1.configure(background = self.sys.win_cfg.cLEDOff)  
        self.update_advanced_led()    
                                  
    def led_advanced(self):
        if (self.c_LEDAdv.winfo_exists() == 1): #window exists
        #close window
            self.c_LEDAdv.close_window()
        else: #open window
            self.w_LEDAdv = Toplevel(self.parent)
            self.c_LEDAdv = NGA_Window_LED_Advanced(self.w_LEDAdv, self.sys)
