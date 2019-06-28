from Tkinter import Label, Entry, BOTH
from ttk import Frame, Button, Style

import time

import os
import tkFileDialog

class NGA_Window_FileInfo(Frame):

    sys = None

    

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)  
        
        self.sys = sys
        self.sys.c_fileinfo_window = self

        self.parent = parent

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wFileinfo)
        self.parent.title(self.sys.win_cfg.sFileinfo)

        # draw window
        self.initUI()

        # window defaults
                

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)
        
        titleLabel = Label(self, text=self.sys.win_cfg.sFileinfo,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)

        # file function buttons
        browseButton = Button(self, text="Browse",
            command=self.browse_folder, width=12)
        browseButton.place(x=15, y=40)
        
        netButton = Button(self, text="Net",
            command=self.net_check, width=8)
        netButton.place(x=125, y=40)
    
        chipIDLabel = Label(self, text="Chip ID: ",
                             background=self.sys.win_cfg.cBackground,
                             width=8, height=1)
        chipIDLabel.place(x=10, y=80)
        self.chipIDEntry = Entry(self, width=15,
                           background=self.sys.win_cfg.cTextBackground)
        self.chipIDEntry.place(x=85, y=80)
        
        self.chipIDEntry.insert(0, self.instant_chip_id())
        
        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=17)
        closeButton.place(x=15, y=140)
        
    def browse_folder(self):
        fold_name = tkFileDialog.askdirectory()
        if os.path.isdir(fold_name):
            print fold_name
        else: print 'No file chosen'

    def instant_chip_id(self):
        return time.strftime("%y%m%d%H%M%S")
    
    def net_check(self):
        self.sys.hw.net.xml_parse()
        print "Net: Enabled: {0:b}".format(self.sys.hw.net.enabled)

    def close_window(self):
        self.parent.destroy()
    
    
