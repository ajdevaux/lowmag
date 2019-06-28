from Tkinter import Label, BOTH
from ttk import Frame, Button, Style

from matplotlib import pyplot as plt

import numpy as np

import time

from NGA_Image.Image import NGA_Image
from NGA_Process.Focus import NGA_Process_Focus

class NGA_Window_Focus(Frame):

    sys = None

    half_tolerance = 0.01
    

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)  
        
        self.sys = sys
        self.sys.c_focus = self

        self.parent = parent

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wFocus)
        self.parent.title(self.sys.win_cfg.sFocus)
        
        # window defaults
        self.img = NGA_Image()

        self.focus = NGA_Process_Focus(self.sys.hw.cam,self.sys.hw.stg)

        # draw window
        self.initUI()

        # window defaults
                

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)
        
        titleLabel = Label(self, text=self.sys.win_cfg.sFocus,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)


        # file function buttons
        coarseFocusButton = Button(self, text="Coarse",
            command=self.coarse_focus, width=17)
        coarseFocusButton.place(x=15, y=40)
        
        fineFocusButton = Button(self, text="Fine",
            command=self.fine_focus, width=17)
        fineFocusButton.place(x=15, y=80)

        halfButton = Button(self, text="Center Corner",
            command=self.center_corner, width=17)
        halfButton.place(x=15, y=120)        
        
        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=17)
        closeButton.place(x=15, y=160)

    def close_window(self):
        self.parent.destroy()
    
    def coarse_focus(self):
        var_a = []
        var_b = []
        var_c = []
        xvals = range(20)
        scores = []
        topscore = 1
        
        self.sys.hw.stg.move_rel_y(-0.01)
	self.sys.c_stage.update_pos_x_y_z()
        start_pos = self.sys.hw.stg.position()[1]

        print "startpos %f" % self.sys.hw.stg.position()[1]
        
        
        start_time = time.time()
        for i in xvals:
            self.sys.hw.stg.move_rel_y(0.001)
            self.update_location()
            self.sys.c_cam.capture_frame()
            scores = np.append(scores,self.focus.score())
            if (scores[i] > scores[topscore-1]):
                topscore = i+1
        print "settle in a final location %f" % (start_pos + topscore*.001)
        self.sys.hw.stg.move_y(start_pos + topscore*.001)
        self.update_location()
        self.sys.c_cam.capture_frame()
        return self.sys.hw.stg.actual_position()[1]
    
    def fine_focus(self):
        print "Focus: Fine"
        
    def update_location(self):
        # if window is closed, don't do mess things up
        if (self.sys.c_stage.winfo_exists() == 1): #window exists
            self.sys.c_stage.update_actual_location()
            self.sys.c_stage.parent.update()

    def find_horizontal_edge(self, start_color):
        self.sys.c_cam.capture_frame()
        thresh = self.focus.brightness()
        #print thresh
        num = thresh
        if start_color == 1:
            while(num > thresh*0.8):
                self.sys.hw.stg.move_rel_x(-0.1)
                self.update_location()
                self.sys.c_cam.capture_frame()
                num = self.focus.brightness()
                #print num, thresh
        elif start_color == 0:
            while(num < thresh*1.2):
                self.sys.hw.stg.move_rel_x(-0.1)
                self.update_location()
                self.sys.c_cam.capture_frame()
                num = self.focus.brightness()
                #print num, thresh
        

    def find_vertical_edge(self, start_color):
        self.sys.c_cam.capture_frame()
        thresh = self.focus.brightness()
        num = thresh
        if start_color == 1:
            while(num > thresh*0.8):
                self.sys.hw.stg.move_rel_y(0.1)
                self.update_location()
                self.sys.c_cam.capture_frame()
                num = self.focus.brightness()
        elif start_color == 0:
            while(num < thresh*1.2):
                self.sys.hw.stg.move_rel_y(0.1)
                self.update_location()
                self.sys.c_cam.capture_frame()
                num = self.focus.brightness()

    def find_horizontal_half(self):
        self.sys.c_cam.capture_frame()
        score = self.focus.percent_dark()
        while(abs(0.5 - score) > self.half_tolerance):
            if (abs(0.5 - score) > 0.1):
                if (score > 0.5):
                    self.sys.hw.stg.move_rel_x(-0.03)
                    self.update_location()
                else:
                    self.sys.hw.stg.move_rel_x(0.03)
                    self.update_location()
            else:
                if (score > 0.5):
                    self.sys.hw.stg.move_rel_x(-0.005)
                    self.update_location()
                else:
                    self.sys.hw.stg.move_rel_x(0.005)
                    self.update_location()
            self.sys.c_cam.capture_frame()
            score = self.focus.percent_dark()
            print score

    def find_vertical_half(self):
        self.sys.c_cam.capture_frame()
        score = self.focus.percent_dark()
        while(abs(0.5 - score) > self.half_tolerance):
            if (abs(0.5 - score) > 0.1):
                if (score > 0.5):
                    self.sys.hw.stg.move_rel_y(-0.03)
                    self.update_location()
                else:
                    self.sys.hw.stg.move_rel_y(0.03)
                    self.update_location()
            else:
                if (score > 0.5):
                    self.sys.hw.stg.move_rel_y(-0.005)
                    self.update_location()
                else:
                    self.sys.hw.stg.move_rel_y(0.005)
                    self.update_location()
            self.sys.c_cam.capture_frame()
            score = self.focus.percent_dark()
            print score

    def center_corner(self):
        self.quad = self.focus.quadrant()
        print self.focus.find_corner(self.quad)
        # while((abs(0.5 - x) > 0.03) | (abs(0.5 - y) > 0.03)):
        #     if(x > 0.5):
        #         self.sys.hw.stg.move_rel_x(-0.01)
        #         self.update_location()
        #     else:
        #         self.sys.hw.stg.move_rel_x(0.01)
        #         self.update_location()
        #     if (y > 0.5):
        #         self.sys.hw.stg.move_rel_y(-0.01)
        #         self.update_location()
        #     else:
        #         self.sys.hw.stg.move_rel_y(0.01)
        #         self.update_location()
        #     self.sys.c_cam.capture_frame()
        #     x,y = self.focus.find_corner(self.quad)


