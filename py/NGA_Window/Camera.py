from Tkinter import Tk, Label, Entry, BOTH, END
from ttk import Frame, Button, Style
from PIL import Image, ImageTk
import time

import numpy as np

from matplotlib import pyplot as plt

from NGA_Image.Image import NGA_Image
from NGA_Image.WImage import NGA_WImage
from NGA_Image.RealTime import NGA_RealTime #for external realtime window

from NGA_Interface.Camera import NGA_Interface_Camera
from NGA_Interface.Client import NGA_Interface_Client

class NGA_Window_Camera(Frame):

    img = None
    sys = None
    rt = None

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)   
        
        self.parent = parent
        self.sys = sys
        # attach handle to this window class to main sys class
        self.sys.c_cam = self

        # set window configurations
        self.parent.geometry(self.sys.win_cfg.wCam)
        self.parent.title(self.sys.win_cfg.sCam)


        # initalize daemon
        self.client = NGA_Interface_Client()
        
        # draw window
        self.initUI()

        # load defaults from self.sys.py_cfg
        self.populate_config()

        # window defaults
        self.img = NGA_Image()

    def update_config(self):
        #self.get_config()
        self.sys.py_cfg.save()
        
    def populate_config(self):
        self.shutterEntry.delete(0, END)
        self.framesEntry.delete(0, END)
        self.shutterEntry.insert(0, self.sys.py_cfg.defaults.config['shutter'])
        self.framesEntry.insert(0, self.sys.py_cfg.defaults.config['frames'])
        
    def get_config(self):
        self.sys.py_cfg.defaults.config['shutter'] = self.shutterEntry.get()
        self.sys.py_cfg.defaults.config['frames'] = self.framesEntry.get()
    
    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        titleLabel = Label(self, text=self.sys.win_cfg.sCam,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)
        
        # setup labels
        self.CameraConfigured = Label(self, width=12,
                                      background=self.sys.win_cfg.cUnknown, text="Not Configured")
        self.CameraConfigured.place(x=20, y=120)
        
        # setup buttons
        shutterLabel = Label(self, text="Shutter (ms): ",
                             background=self.sys.win_cfg.cBackground,
                             width=9, height=1)
        shutterLabel.place(x=10, y=30)
        self.shutterEntry = Entry(self, width=5,
                           background=self.sys.win_cfg.cTextBackground)
        self.shutterEntry.place(x=85, y=30)

        framesLabel = Label(self, text="Frames (#): ",
                             background=self.sys.win_cfg.cBackground,
                             width=9, height=1)
        framesLabel.place(x=10, y=60)
        self.framesEntry = Entry(self, width=5,
                           background=self.sys.win_cfg.cTextBackground)
        self.framesEntry.place(x=85, y=60)
        
        setupCameraButton = Button(self, text="Setup Camera",
            command=self.setup_camera, width=14)
        setupCameraButton.place(x=20, y=90)
       
        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=14)
        closeButton.place(x=20, y=350)

        ## 2nd column
        captureButton = Button(self, text="Capture Frame",
            command=self.capture_frame, width=14)
        captureButton.place(x=20, y=150)
        histButton = Button(self, text="Histogram",
            command=self.histogram, width=14)
        histButton.place(x=20, y=180)
        #rapid10Button = Button(self, text="Repeat 10",
        #    command=self.rapid10, width=14)
        #rapid10Button.place(x=20, y=210)
        #autoContrastButton = Button(self, text="Auto Contrast",
        #    command=self.autocontrast, width=14)
        #autoContrastButton.place(x=20, y=240)

        realTimeButton = Button(self, text="RealTime",
            command=self.real_time, width=14)
        realTimeButton.place(x=20, y=270)

    def camera_configured(self):
        self.CameraConfigured.configure(background=self.sys.win_cfg.cGood, text="Configured")
        print "PointGrey: One Camera Detected and Configured"
    def camera_unconfigured_button(self):
        self.CameraConfigured.configure(background=self.sys.win_cfg.cBad, text="Not Configured")
        self.update()
    def camera_unconfigured(self):
        if (self.sys.hw.cam.cam_detected == 0):
            print "PointGrey: NO CAMERAS DETECTED"
        else:
            print "PointGrey: TOO MANY cameras detected"
    
    def incorporate_py_config(self):
        for key in self.sys.hw.cam.cam_config.defaults.config:
            if (key == "shutter"):
                self.sys.hw.cam.cam_config.defaults.config['shutter'] = self.sys.py_cfg.defaults.config['shutter']
            if (key == "frames"):
                # frames is special, it's value was stored and will overwrite in
                # NGA_Interface_Camera
                self.sys.hw.cam.cam_config.defaults.config['frames'] = self.sys.py_cfg.defaults.config['frames']
                self.sys.hw.cam.frms = self.sys.py_cfg.defaults.config['frames']
    
    def close_window(self):
        self.img.imclose()
        self.parent.destroy()
    
    def setup_camera(self):
        if (self.client.connected == 0):
            self.client.connect()
        self.camera_unconfigured_button()
        self.get_config()
        self.sys.hw.cam = NGA_Interface_Camera(self.client)
        self.incorporate_py_config()

        self.update_config() #save python variables (shutter/frames)
        if (self.sys.hw.cam.cam_error == False):
            self.camera_configured()
        else:
            self.camera_unconfigured()
            
    def capture_frame(self):
        start_time = time.time()
        self.get_config()
        self.incorporate_py_config()
        self.sys.hw.cam.image()
        elapsed_time = time.time() - start_time
        str_cap = "cap: {0:.2f} s.".format(elapsed_time)
        self.CameraConfigured.configure(text=str_cap)

        
        
##        self.img.imclose()
##        self.img.load()
##        self.img.imshow()
        #self.show_cap_frame()
    def quitDaemon(self):
        self.sys.hw.cam.quitCamera()
        
    def show_cap_frame(self):
        self.wimg = NGA_WImage()
        self.wimg.draw()
    def autocontrast(self):
        self.camera_unconfigured_button()
        self.get_config()
        self.sys.hw.cam = NGA_Interface_Camera()
        self.incorporate_py_config()

        self.sys.hw.cam.clean_image()
        self.update_config() #save python variables (shutter/frames)
        var_a = []
        var_b = []
        var_c = []
        xvals = range(10)
        xvals_vals = []
        for i in xvals:
            xvals_vals = np.append(xvals_vals,i*10+10)
            self.sys.hw.cam.cam_config.defaults.config['shutter'] = str(xvals_vals[i])
            self.sys.hw.cam.clean_image()
            self.sys.hw.cam.image()
            self.img.load()
            var_a = np.append(var_a,self.img.info.config['intensity'])
            var_b = np.append(var_b,self.img.info.config['quality'])
            var_c = np.append(var_c,self.img.info.config['n_variance'])

        plt.plot(xvals_vals,var_a,label='Intensity')
        plt.plot(xvals_vals,var_b,label='Quality')
        plt.plot(xvals_vals,var_c,label='Variance')
        plt.yscale('log')
        legend = plt.legend(loc='upper center', shadow=True)
        plt.show()
        
        if (self.sys.hw.cam.cam_error == False):
            self.camera_configured()
        else:
            self.camera_unconfigured()

        print "Camera: Autocontrast complete"
        
    def histogram(self):
        self.img.imhist()
    def real_time(self):
        self.rt = NGA_RealTime()
    def close_realtime(self):
        if(self.rt):
            self.rt.close()
    def rapid10(self):
        self.rapid(10)
    def rapid50(self):
        self.rapid(50)
    def rapid(self, frms):
        frames = frms
        self.img.imclose()
        start_time = time.time()
        for n in range(1, frames):
            self.sys.hw.cam = NGA_Interface_Camera()
            self.incorporate_py_config()
            self.sys.hw.cam.image()
            self.img.load()
            self.img.imshow()
        elapsed_time = time.time() - start_time
        print("{0:.1f} fps".format(frames/elapsed_time))
