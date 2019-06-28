from Tkinter import Label, Entry, Checkbutton, IntVar, BOTH, END
from ttk import Frame, Button, Style

import time
import os

from datetime import datetime

class NGA_Window_Stage(Frame):

    stage = None
    x_val = 0.0
    y_val = 0.0
    z_val = 0.0
    actual_x_val = 0.0
    actual_y_val = 0.0
    actual_z_val = 0.0
    x_jog = 0.100
    y_jog = 0.100
    z_jog = 0.05000
    x_status = None
    y_status = None
    z_status = None
    
    x_return_pos = True
    y_return_pos = True
    z_return_pos = True

    height = 1
    row = 1
    col = 1
    run = 1
    
    chkAutoUpdate = None
    
    sys = None
    

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.sys = sys
        # attach handle to this window class to main sys class
        self.sys.c_stage = self
        
        # force reloading of stage config upon redrawing stage window
        self.sys.hw.reload_stage()

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wStage)
        self.parent.title(self.sys.win_cfg.sStage)

        # draw window
        self.initUI()

        # window defaults       
        self.load_config()
        
    def load_config(self):
        stage_txt = "Stage: {0}".format(self.sys.hw.stg.stage_name())
        self.StageConfigured.configure(text = stage_txt)
        if (self.sys.hw.stg.stage_name() == "virtual"):
            self.StageConfigured.configure(background=self.sys.win_cfg.cBad)
        else:
            self.StageConfigured.configure(background=self.sys.win_cfg.cGood)
        
        # need to do this first to populate stage settgins
        self.update_actual_location()
        
        #on loading, set the desired locations to the actual locations
        self.sys.hw.stg.stage.x_pos = self.sys.hw.stg.stage.actual_x_pos
        self.sys.hw.stg.stage.y_pos = self.sys.hw.stg.stage.actual_y_pos
        self.sys.hw.stg.stage.z_pos = self.sys.hw.stg.stage.actual_z_pos
        
        self.update_pos_x_y_z()
        self.update_jog_x_y_z()

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        titleLabel = Label(self, text=self.sys.win_cfg.sStage,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)
        
        # setup labels
        self.StageConfigured = Label(self, width=15, 
                                      background=self.sys.win_cfg.cUnknown, text="Not Configured")
        self.StageConfigured.place(x=100, y=5)
        
        
        yoffset = 20
        #right column
        self.xActualLabel = Label(self, text="",
                             background=self.sys.win_cfg.cTextBackgroundLocked,
                             width=10, height=1)
        self.xActualLabel.place(x=200, y=30+yoffset)
        
        self.yActualLabel = Label(self, text="",
                             background=self.sys.win_cfg.cTextBackgroundLocked,
                             width=10, height=1)
        self.yActualLabel.place(x=200, y=60+yoffset)
        
        self.zActualLabel = Label(self, text="",
                             background=self.sys.win_cfg.cTextBackgroundLocked,
                             width=10, height=1)
        self.zActualLabel.place(x=200, y=90+yoffset)
        
        
        self.xMovingLabel = Label(self, width=3, background=self.sys.win_cfg.cStageMoving, text="X")
        self.xMovingLabel.place(x=270, y=30+yoffset)
        
        self.yMovingLabel = Label(self, width=3, background=self.sys.win_cfg.cStageMoving, text="Y")
        self.yMovingLabel.place(x=270, y=60+yoffset)
        
        self.zMovingLabel = Label(self, width=3, background=self.sys.win_cfg.cStageMoving, text="Z")
        self.zMovingLabel.place(x=270, y=90+yoffset)
        
        '''
        self.chkAutoUpdate = IntVar()
        self.chkAutoUpdate.set(1)
        self.autoUpdateCheckbutton = Checkbutton(self, text="Auto Update",
                                                 backgroun=self.sys.win_cfg.cBackground,
                                                 variable=self.chkAutoUpdate)
        self.autoUpdateCheckbutton.place(x=200, y=120+yoffset)
        '''

        self.testButton = Button(self, text="test",
            command=self.testNight, width=10)
        self.testButton.place(x=200, y=130+yoffset)
        
        locationButton = Button(self, text="Location",
            command=self.update_actual_location, width=10)
        locationButton.place(x=200, y=160+yoffset)
        
        lockButton = Button(self, text="Lock",
            command=self.lock, width=10)
        lockButton.place(x=200, y=190+yoffset)
        unlockButton = Button(self, text="Unlock",
            command=self.unlock, width=10)
        unlockButton.place(x=200, y=220+yoffset)
        
        style = Style()
        style.configure("Red.TButton", foreground=self.sys.win_cfg.cBad,
                        background=self.sys.win_cfg.cBad)
        
        abortButton = Button(self, text="\nAbort!\n",
            command=self.abort_stage, width=10)
        abortButton.configure(style="Red.TButton")
        abortButton.place(x=200, y=280+yoffset)

        # setup buttons
        xLabel = Label(self, text="X (mm): ",
                             background=self.sys.win_cfg.cBackground,
                             width=6, height=1)
        xLabel.place(x=10, y=30+yoffset)
        self.xEntry = Entry(self, width=12,
                           background=self.sys.win_cfg.cTextBackground)
        self.xEntry.place(x=85, y=30+yoffset)

        yLabel = Label(self, text="Y (mm): ",
                             background=self.sys.win_cfg.cBackground,
                             width=6, height=1)
        yLabel.place(x=10, y=60+yoffset)
        self.yEntry = Entry(self, width=12,
                           background=self.sys.win_cfg.cTextBackground)
        self.yEntry.place(x=85, y=60+yoffset)
        zLabel = Label(self, text="Z (mm): ",
                             background=self.sys.win_cfg.cBackground,
                             width=6, height=1)
        zLabel.place(x=10, y=90+yoffset)
        self.zEntry = Entry(self, width=12,
                           background=self.sys.win_cfg.cTextBackground)
        self.zEntry.place(x=85, y=90+yoffset)
        
        
        


        # buttons
        moveStagesButton = Button(self, text="Move Stages",
            command=self.move_stages, width=17)
        moveStagesButton.place(x=30, y=120+yoffset)

        homeStagesButton = Button(self, text="Home Stages ",
            command=self.home_stages, width=17)
        homeStagesButton.place(x=30, y=260+yoffset)

        homeStageButton = Button(self, text="Scan Array ",
            command=self.scan_array, width=10)
        homeStageButton.place(x=30, y=295+yoffset)
        self.frameCount = Entry(self, width=5,
                           background=self.sys.win_cfg.cTextBackground)
        self.frameCount.place(x=110, y=298+yoffset)

        # buttons
        JogXPlusButton = Button(self, text="X +",
            command=self.jog_x_up, width=5)
        JogXPlusButton.place(x=10, y=160+yoffset)
        
        self.JogX = Entry(self, width=8,
                           background=self.sys.win_cfg.cTextBackground)
        self.JogX.place(x=65, y=163+yoffset)
        
        JogXMinuxButton = Button(self, text="X -",
            command=self.jog_x_down, width=5)
        JogXMinuxButton.place(x=130, y=160+yoffset)

        JogYPlusButton = Button(self, text="Y +",
            command=self.jog_y_up, width=5)
        JogYPlusButton.place(x=10, y=190+yoffset)
        
        self.JogY = Entry(self, width=8,
                           background=self.sys.win_cfg.cTextBackground)
        self.JogY.place(x=65, y=193+yoffset)
        
        JogYMinuxButton = Button(self, text="Y -",
            command=self.jog_y_down, width=5)
        JogYMinuxButton.place(x=130, y=190+yoffset)
        
        JogZPlusButton = Button(self, text="Z +",
            command=self.jog_z_up, width=5)
        JogZPlusButton.place(x=10, y=220+yoffset)
        
        self.JogZ = Entry(self, width=8,
                           background=self.sys.win_cfg.cTextBackground)
        self.JogZ.place(x=65, y=223+yoffset)
        
        JogZMinuxButton = Button(self, text="Z -",
            command=self.jog_z_down, width=5)
        JogZMinuxButton.place(x=130, y=220+yoffset)
        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=17)
        closeButton.place(x=30, y=350)
        
        
        # on absolute entries only, enter key moves to positions
        self.xEntry.bind("<KeyRelease-Return>", self.move_stages_return)
        self.yEntry.bind("<KeyRelease-Return>", self.move_stages_return)
        self.zEntry.bind("<KeyRelease-Return>", self.move_stages_return)
        # on absolute entries only, enter key moves to positions
        self.JogX.bind("<KeyRelease-Return>", self.jog_x_return)
        self.JogY.bind("<KeyRelease-Return>", self.jog_y_return)
        self.JogZ.bind("<KeyRelease-Return>", self.jog_z_return)
        
        self.JogX.bind("<KeyRelease-Shift_L>", self.jog_x_inverse)
        self.JogX.bind("<KeyRelease-Shift_R>", self.jog_x_inverse)
        self.JogY.bind("<KeyRelease-Shift_L>", self.jog_y_inverse)
        self.JogY.bind("<KeyRelease-Shift_R>", self.jog_y_inverse)
        self.JogZ.bind("<KeyRelease-Shift_L>", self.jog_z_inverse)
        self.JogZ.bind("<KeyRelease-Shift_R>", self.jog_z_inverse)

     
    def jog_x_up(self):
        self.jog_x_y_z_up_down('x', True)
        self.x_return_pos = True
    def jog_x_down(self):
        self.jog_x_y_z_up_down('x', False)
        self.x_return_pos = False
    def jog_y_up(self):
        self.jog_x_y_z_up_down('y', True)
        self.y_return_pos = True
    def jog_y_down(self):
        self.jog_x_y_z_up_down('y', False)
        self.y_return_pos = False
    def jog_z_up(self):
        self.jog_x_y_z_up_down('z', True)
        self.z_return_pos = True
    def jog_z_down(self):
        self.jog_x_y_z_up_down('z', False)
        self.z_return_pos = False   
              
    def jog_x_y_z_up_down(self, xyz_str, up = True):
        if (xyz_str == 'x'):
            xval = float(self.JogX.get())
            if (up == True):
                self.x_jog = xval 
                self.x_val = self.x_val + xval                
            else:
                self.x_jog = -1*xval
                self.x_val = self.x_val - xval
            self.sys.hw.stg.move_x(self.x_val)
        elif (xyz_str == 'y'):
            yval = float(self.JogY.get())
            if (up == True):
                self.y_jog = yval
                self.y_val = self.y_val + yval                
            else:
                self.y_jog = -1*yval
                self.y_val = self.y_val - yval
            self.sys.hw.stg.move_y(self.y_val)
        elif (xyz_str == 'z'):
            zval = float(self.JogZ.get())
            if (up == True):
                self.z_jog = -zval
                self.z_val = self.z_val + zval                
            else:
                self.z_jog = -1*zval
                self.z_val = self.z_val - zval
            self.sys.hw.stg.move_z(self.z_val)
        self.update_pos_x_y_z()
        
    def update_pos_x_y_z(self):
        
        [self.x_val, self.y_val, self.z_val] = self.sys.hw.stg.position()
        self.xEntry.delete(0, END)
        self.xEntry.insert(0, "{0:.6f}".format(self.x_val))
        self.yEntry.delete(0, END)
        self.yEntry.insert(0, "{0:.6f}".format(self.y_val))
        self.zEntry.delete(0, END)
        self.zEntry.insert(0, "{0:.6f}".format(self.z_val))
        self.check_auto_update_location()

    def update_jog_x_y_z(self):
        
        #[self.x_val, self.y_val, self.z_val] = self.sys.hw.stg.position()
        self.JogX.delete(0, END)
        self.JogX.insert(0, "{0:.6f}".format(self.x_jog))
        self.JogY.delete(0, END)
        self.JogY.insert(0, "{0:.6f}".format(self.y_jog))
        self.JogZ.delete(0, END)
        self.JogZ.insert(0, "{0:.6f}".format(self.z_jog))

    def check_auto_update_location(self):
        #if (self.chkAutoUpdate.get() == 1):
            self.update_actual_location()
            self.parent.update()
            try:
                #print "Moving: "
                #print self.x_status['axis_moving']
                while ( (self.x_status['axis_moving'] == True) |
                    (self.y_status['axis_moving'] == True) |
                    (self.z_status['axis_moving'] == True) ):
                    self.update_actual_location()
                    self.parent.update()
                    time.sleep(0.05)
                    # don't mess things up here
            except:
                print "Fix this!;"
            
    def close_window(self):
        self.parent.destroy()

    def lock(self):
        self.sys.hw.stg.program12() 
        
    def unlock(self):
        self.sys.hw.stg.program13() 
        
    def home_stages(self):
        self.sys.hw.stg.home()   
        self.update_pos_x_y_z()    
        self.sys.hw.stg.zero() #reset position after done moving
        self.update_pos_x_y_z() #load in the 0 value  
            
    def scan_array(self):
        for i in range(1,7):
            self.scan_col(i%2)
            self.sys.hw.stg.move_rel_z(-.282)
            self.row += 1
        

    def scan_col(self, mode):
        self.col = 0;
        for i in range(1,8):
            self.scan_stack(i%2)
            if(i != 7):
                self.sys.hw.stg.move_rel_x(.282*pow(-1,mode))
            self.col += 1
            print i;
            

    def scan_stack(self, mode):
        self.height = 0;
	self.sys.c_stage.update_pos_x_y_z()
        start_pos = self.sys.hw.stg.position()[1]
        self.sys.c_focus.coarse_focus()
        for i in range(0,50):
            for j in range(0,int(self.frameCount.get())):
                self.sys.hw.cam.image()
                filename = r"..\data\capture_py-%d-%d-%d.png" % (self.col, self.row, self.height)
                os.rename(r"..\data\capture_py.png", filename)
                self.height += 1
            if (i == 49):
                self.sys.hw.stg.move_y(start_pos)
            else:
                self.sys.hw.stg.move_rel_y(-.0005)
            
    def testNight(self):
        self.testButton["text"] ="stop"
        self.testButton["command"] = self.stopRun
        self.run = 1
        while(self.run):
            if(self.sys.hw.stg.check_err() == 0):
                self.sys.hw.stg.move_y(-25)
                self.update_pos_x_y_z()
                if(self.run):
                    self.sys.hw.stg.move_y(25)
                    self.update_pos_x_y_z()
            else:
                self.run = 0

    def stopRun(self):
        self.run = 0
        self.testButton["text"] ="test"
        self.testButton["command"] = self.testNight
        
    # caller for TKinter Edit Box      
    def move_stages_return(self,event):
        self.move_stages()
        
    # caller for TKinter Edit Box      
    def jog_x_return(self,event):
        self.jog_x_y_z_up_down('x', self.x_return_pos)
        
    # caller for TKinter Edit Box      
    def jog_y_return(self,event):
        self.jog_x_y_z_up_down('y', self.y_return_pos)
        
    # caller for TKinter Edit Box      
    def jog_z_return(self,event):
        self.jog_x_y_z_up_down('z', self.z_return_pos)
    
    # caller for TKinter Edit Box      
    def jog_x_inverse(self,event):
        if (self.x_return_pos == True):
            self.x_return_pos = False
        else: 
            self.x_return_pos = True
            
    # caller for TKinter Edit Box      
    def jog_y_inverse(self,event):
        if (self.y_return_pos == True):
            self.y_return_pos = False
        else: 
            self.y_return_pos = True
            
    # caller for TKinter Edit Box      
    def jog_z_inverse(self,event):
        if (self.z_return_pos == True):
            self.z_return_pos = False
        else: 
            self.z_return_pos = True
        
    def move_stages(self):
        xval = float(self.xEntry.get())
        yval = float(self.yEntry.get())
        zval = float(self.zEntry.get())
        self.sys.hw.stg.move_x(xval)
        self.sys.hw.stg.move_y(yval)
        self.sys.hw.stg.move_z(zval)
        self.update_pos_x_y_z()
        
    def update_actual_location(self):
        [x_val, y_val, z_val] = self.sys.hw.stg.actual_position()
        #self.xActualLabel.update(0, END)
        self.actual_x_val = x_val
        self.actual_y_val = y_val
        self.actual_z_val = z_val
        self.xActualLabel.configure(text="{0:.6f}".format(self.actual_x_val))
        self.yActualLabel.configure(text="{0:.6f}".format(self.actual_y_val))
        self.zActualLabel.configure(text="{0:.6f}".format(self.actual_z_val))
        
        self.x_status = self.sys.hw.stg.status_x()
        self.y_status = self.sys.hw.stg.status_y()
        self.z_status = self.sys.hw.stg.status_z()
        '''
        '''
        if (self.x_status['axis_enabled'] == True):
            if (self.x_status['axis_moving'] == True):
                self.xMovingLabel.configure(background = self.sys.win_cfg.cStageMoving)
            else:
                self.xMovingLabel.configure(background = self.sys.win_cfg.cStageNotMoving)
        else: 
            self.xMovingLabel.configure(background = self.sys.win_cfg.cStageDisabled)
        
        if (self.y_status['axis_enabled'] == True):
            if (self.y_status['axis_moving'] == True):
                self.yMovingLabel.configure(background = self.sys.win_cfg.cStageMoving)
            else:
                self.yMovingLabel.configure(background = self.sys.win_cfg.cStageNotMoving)
        else: 
            self.yMovingLabel.configure(background = self.sys.win_cfg.cStageDisabled)
        
        if (self.z_status['axis_enabled'] == True):
            if (self.z_status['axis_moving'] == True):
                self.zMovingLabel.configure(background = self.sys.win_cfg.cStageMoving)
            else:
                self.zMovingLabel.configure(background = self.sys.win_cfg.cStageNotMoving)
        else: 
            self.zMovingLabel.configure(background = self.sys.win_cfg.cStageDisabled)
        
        #print "{0:.6f},{1:.6f},{2:.6f}".format(x_val, y_val, z_val)
        
    def setup_stages(self):
        pass

    def abort_stage(self):
        self.sys.hw.stg.abort()
        # uncomment below for testing the home & zero functionality
        #self.sys.hw.stg.zero() #reset position after done moving
        
