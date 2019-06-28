from Tkinter import Tk, Label, Entry, BOTH, END
from ttk import Frame, Button, Style

from NGA_Interface.LED import NGA_Interface_LED

class NGA_Window_LED_Advanced(Frame):

    led = None
    
    led1amp = 100.0
    led2amp = 100.0
    led3amp = 100.0
    led4amp = 100.0
    
    sys = None

    wLED = None #window of pointer to main LED window
  
    def __init__(self, parent, sys):
        Frame.__init__(self, parent)  
         
        #self.wLED = sys.wL #LED Window
        self.parent = parent
        self.sys = sys
        self.sys.c_led_advanced = self

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wLEDAdvanced)
        self.parent.title(self.sys.win_cfg.sLEDAdvanced)

        # draw window
        self.initUI()

        # window defaults
        self.update_led_on_off() 
        
    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)


        # setup labels
        self.LED1 = Label(self, width=4, background=self.sys.win_cfg.cLEDOff, text="LED1")
        self.LED1.place(x=98, y=45)
        self.LED2 = Label(self, width=4, background=self.sys.win_cfg.cLEDOff, text="LED2")
        self.LED2.place(x=98, y=75)
        self.LED3 = Label(self, width=4, background=self.sys.win_cfg.cLEDOff, text="LED3")
        self.LED3.place(x=98, y=105)
        self.LED4 = Label(self, width=4, background=self.sys.win_cfg.cLEDOff, text="LED4")
        self.LED4.place(x=98, y=135)
        
        # setup entries
        
        titleLabel = Label(self, text=self.sys.win_cfg.sLEDAdvanced,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)
        percentLabel = Label(self, text="0-100 (%)",
                             background=self.sys.win_cfg.cBackground,
                             width=8, height=1)
        percentLabel.place(x=5, y=22)
        self.led1val = Entry(self, width=4, 
                           background=self.sys.win_cfg.cTextBackground)
        self.led1val.place(x=10, y=50-4)
        self.led2val = Entry(self, width=4,
                           background=self.sys.win_cfg.cTextBackground)
        self.led2val.place(x=10, y=80-4)
        self.led3val = Entry(self, width=4,
                           background=self.sys.win_cfg.cTextBackground)
        self.led3val.place(x=10, y=110-4)
        self.led4val = Entry(self, width=4,
                           background=self.sys.win_cfg.cTextBackground)
        self.led4val.place(x=10, y=140)
        
        # setup buttons
        led1onButton = Button(self, text="LED1",
            command=self.led1_on,  width=6)
        led1onButton.place(x=45, y=45)
        led2onButton = Button(self, text="LED2",
            command=self.led2_on,  width=6)
        led2onButton.place(x=45, y=75)
        led3onButton = Button(self, text="LED3",
            command=self.led3_on,  width=6)
        led3onButton.place(x=45, y=105)
        led4onButton = Button(self, text="LED4",
            command=self.led4_on,  width=6)
        led4onButton.place(x=45, y=135)

        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window)
        closeButton.place(x=30, y=180)
        
        self.update_duty()

    def update_duty(self):
        self.led1val.delete(0, END)
        self.led1val.insert(0, "{0:.1f}".format(self.led1amp))
        self.led2val.delete(0, END)
        self.led2val.insert(0, "{0:.1f}".format(self.led2amp))
        self.led3val.delete(0, END)
        self.led3val.insert(0, "{0:.1f}".format(self.led3amp))
        self.led4val.delete(0, END)
        self.led4val.insert(0, "{0:.1f}".format(self.led4amp))
        
    def getValues(self):
        self.led1amp = float(self.led1val.get())
        self.led2amp = float(self.led2val.get())
        self.led3amp = float(self.led3val.get())
        self.led4amp = float(self.led4val.get())
        
    def byteFromPer(self, val):
        return val*(255.0/100.0) #percent (0-100) to (0-255)
    def close_window(self):
        self.parent.destroy()
    def led1_on(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        self.getValues()
        self.sys.hw.led.duty_cycle(0,self.byteFromPer(self.led1amp))
        self.update_regular_led()
    def led2_on(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        self.getValues()
        self.sys.hw.led.duty_cycle(1,self.byteFromPer(self.led2amp))
        self.update_regular_led() 
    def led3_on(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        self.getValues()
        self.sys.hw.led.duty_cycle(2,self.byteFromPer(self.led3amp))
        self.update_regular_led()                          
    def led4_on(self):
        self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
        self.getValues()
        self.sys.hw.led.duty_cycle(3,self.byteFromPer(self.led4amp))
        self.update_regular_led()
        
    def update_led_on_off(self):
        if self.sys.hw.led.led_on[0] == True:
            self.LED1.configure(background = self.sys.win_cfg.cLEDOn)
        if self.sys.hw.led.led_on[0] == False:
            self.LED1.configure(background = self.sys.win_cfg.cLEDOff)
        if self.sys.hw.led.led_on[1] == True:
            self.LED2.configure(background = self.sys.win_cfg.cLEDOn)
        if self.sys.hw.led.led_on[1] == False:
            self.LED2.configure(background = self.sys.win_cfg.cLEDOff) 
        if self.sys.hw.led.led_on[2] == True:
            self.LED3.configure(background = self.sys.win_cfg.cLEDOn)
        if self.sys.hw.led.led_on[2] == False:
            self.LED3.configure(background = self.sys.win_cfg.cLEDOff) 
        if self.sys.hw.led.led_on[3] == True:
            self.LED4.configure(background = self.sys.win_cfg.cLEDOn)
        if self.sys.hw.led.led_on[3] == False:
            self.LED4.configure(background = self.sys.win_cfg.cLEDOff)  
            
    def update_regular_led(self):
        if (self.parent.winfo_exists() == 1): #window exists
            self.sys.c_led.update_led() # inform led window        
        self.update_led_on_off() 
            
        
    def update_led(self):
        self.update_led_on_off()

