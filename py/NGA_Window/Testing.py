from Tkinter import Tk, Label, BOTH, Toplevel
from ttk import Frame, Button, Style
import time
import datetime
from datetime import date
import cv2

from NGA_Window.Camera import NGA_Window_Camera
from NGA_Interface.LED import NGA_Interface_LED

class NGA_Window_Testing(Frame):

    running = 0;
    
    f = 0
    
    def __init__(self, parent,sys):
        Frame.__init__(self,parent)

        self.parent = parent
        self.sys = sys
    
        self.sys.c_test = self
        
        self.parent.geometry(self.sys.win_cfg.wTesting)
        self.parent.title(self.sys.win_cfg.sTesting)
        
        self.initUI()

    def initUI(self):
        
        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        self.runTestButton = Button(self, text="Run Test",
                               command=self.runTest, width = 20)
        self.runTestButton.place(x=20,y=20)

        self.runKoreanButton = Button(self, text="Run Korean",
                                      command=self.runKorean, width = 20)
        self.runKoreanButton.place(x=20,y=50)

    def runTest(self):
        ## DSF, use now time so log isn't overwritten
        dt = datetime.datetime.now()
        self.f = open(str("../testOutput-{}.txt".format(dt.strftime("%y-%m-%d-%H-%M-%S"))), 'w')
        self.runTestButton["text"] = "Stop Test"
        self.runTestButton["command"] = self.stopTest
        #self.sys.c_stage.home_stages()
        self.sys.hw.stg.move_z(-5)
        self.running = 1;
        camerr = 0
        stgerr = 1
        msperr = 1
        roi = [256,256,100,100]
        self.fwrite(str('Running test {} '.format(date.today().strftime("%d/%m/%y"))))
        while(self.running):
            #print str(camerr) + '\n'
            if(camerr == 0):
                try:
                    for i in range(0,10):
                        roi = [1920,1200,0,0]
                        self.fwrite('Acquiring image ROI')
                        self.fwrite('{} {} {} {}'.format(roi[0],roi[1],roi[2],roi[3]))
                        self.sys.hw.cam.image(2,roi)
                        roi = [256,256,100,100]
                        self.fwrite('Acquiring image ROI')
                        self.fwrite('{} {} {} {}'.format(roi[0],roi[1],roi[2],roi[3]))
                        self.sys.hw.cam.image(2,roi)
                except:
                    print 'CAMERA MESSED UP'
                    camerr = 1
            #print str(stgerr) + '\n'
            if(stgerr == 0):
                try:
                    err = self.sys.hw.stg.check_err()
                    if(err == 0):
                        pos = [12.5,25,5]
                        self.fwrite('Moving Stages: x: {} y: {} z: {}'.format(pos[0],pos[1],pos[2]))
                        self.fwrite(self.sys.hw.stg.move_x(pos[0]))
                        self.fwrite(self.sys.hw.stg.move_y(pos[1]))
                        #self.fwrite(self.sys.hw.stg.move_z(pos[2]))
                        self.sys.c_stage.update_pos_x_y_z()
                        err = self.sys.hw.stg.check_err()
                        if(err == 0):
                            pos = [-12.5,-25,-5]
                            self.fwrite('Moving Stages: x: {} y: {} z: {}'.format(pos[0],pos[1],pos[2]))
                            self.fwrite(self.sys.hw.stg.move_x(pos[0]))
                            self.fwrite(self.sys.hw.stg.move_y(pos[1]))
                            #self.fwrite(self.sys.hw.stg.move_z(pos[2]))
                            self.sys.c_stage.update_pos_x_y_z()
                        else:
                            stgerr = 1
                            self.fwrite(err)
                    else:
                        stgerr = 1
                        self.fwrite(err)
                    
                except:
                    print 'STAGES MESSED UP'
                    err = self.sys.hw.stg.check_err()
                    self.fwrite(err)
                    stgerr = 1
                #print str(msperr) + '\n'
            if(msperr == 0):
                try:
                    self.fwrite('Testing LCD')
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD1))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD2))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD3))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD4))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD5))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD6))
                    time.sleep(1)
                    self.fwrite(self.sys.hw.led.command(NGA_Interface_LED.LCD7))
                    time.sleep(1)
                    self.fwrite('Testing LED')
                    self.sys.c_led.led_on()
                    time.sleep(1)
                    self.sys.c_led.led_off()
                    time.sleep(1)
                    self.fwrite('Testing VAC')
                    self.fwrite(self.sys.c_pneumatics.valve_toggle())
                    self.fwrite(self.sys.c_pneumatics.vacuum_toggle())
                    for i in range(0,5):
                        self.fwrite(self.sys.c_pneumatics.measure_pressure())
                        print str(self.sys.c_pneumatics.pressure_val) + '\n'
                        time.sleep(1)
                    self.fwrite(self.sys.c_pneumatics.measure_pressure())
                    temp = self.sys.c_pneumatics.pressure_val
                    self.fwrite(self.sys.c_pneumatics.vacuum_toggle())
                    i = 0
                    while (temp < -10):
                        time.sleep(1)
                        self.fwrite(self.sys.c_pneumatics.measure_pressure())
                        temp = self.sys.c_pneumatics.pressure_val
                        print str(temp) + '\n'
                    self.fwrite(self.sys.c_pneumatics.valve_toggle())
                except:
                    msperr = 1

    def fwrite(self,message):
        output = '{}: {}\n'.format(datetime.datetime.now().time().strftime("%H:%M:%S:%f %Z"),message)
        s = str(output)
        self.f.write(s)

    def stopTest(self):
        self.running = 0;
        self.runTestButton["text"] = "Run Test"
        self.runTestButton["command"] = self.runTest

    def runKorean(self):
        roi = [1920,1200,0,0]
        for i in range(1,50):
            savestr = "jon_" + str(i)
            self.sys.hw.cam.fn = savestr
            self.sys.hw.cam.image()
            
