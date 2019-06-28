from Tkinter import Tk, Label, Entry, OptionMenu, StringVar, BOTH
from ttk import Frame, Button, Style

import os

from NGA_Interface.Process import NGA_Interface_Process
from NGA_Interface.IRIS import NGA_Interface_IRIS

from NGA_Image.WImage import NGA_WImage


class NGA_Window_Process(Frame):

    process = None
    cur_fn = ""
    sys = None

    def __init__(self, parent, sys):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.sys = sys
        # attach handle to this window class to main sys class
        self.sys.c_process = self

        # get window configurations
        self.parent.geometry(self.sys.win_cfg.wProcess)
        self.parent.title(self.sys.win_cfg.sProcess)

        # draw window
        self.initUI()

        # load defaults
        self.populate_config()

        # window defaults
        self.process = NGA_Interface_Process()

        #self.spotfind_low_mag()

    def update_config(self):
        self.sys.py_cfg.save()
        
    def populate_config(self):
        pass
        #self.contrastEntry.insert(0, self.sys.py_cfg.defaults.config['contrast'])
        #self.gaussianEntry.insert(0, self.sys.py_cfg.defaults.config['gaussian'])
        
    def get_config(self):
        pass
        #self.sys.py_cfg.defaults.config['contrast'] = self.contrastEntry.get()
        #self.sys.py_cfg.defaults.config['gaussian'] = self.gaussianEntry.get()
    
    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)
        
        titleLabel = Label(self, text=self.sys.win_cfg.sProcess,
                             background=self.sys.win_cfg.cBackground,
                             width=12, height=1)
        titleLabel.place(x=5, y=5)

        # setup labels
        self.processResult = Label(self, width=12,
                                      background=self.sys.win_cfg.cUnknown, text="            ")
        self.processResult.place(x=20, y=170)
        self.countResult = Label(self, width=8,
                                      background=self.sys.win_cfg.cUnknown, text="0")
        self.countResult.place(x=120, y=170)
        self.extraInfoResult = Label(self, width=22,
                                      background=self.sys.win_cfg.cUnknown, text="")
        self.extraInfoResult.place(x=20, y=200)
        
        # setup buttons
        '''
        contrastLabel = Label(self, text="Contrast: ",
                             background=self.sys.win_cfg.cBackground,
                             width=9, height=1)
        contrastLabel.place(x=10, y=20)
        self.contrastEntry = Entry(self, width=5,
                           background=self.sys.win_cfg.cTextBackground)
        self.contrastEntry.place(x=85, y=20)

        gaussianLabel = Label(self, text="Gaussian: ",
                             background=self.sys.win_cfg.cBackground,
                             width=9, height=1)
        gaussianLabel.place(x=10, y=50)
        self.gaussianEntry = Entry(self, width=5,
                           background=self.sys.win_cfg.cTextBackground)
        self.gaussianEntry.place(x=85, y=50)
        '''
        self.fileListVariable = StringVar(self)
        self.fileListVariable.set("one") # default value
        self.fileListOptionMenu = OptionMenu(self, self.fileListVariable, "one", "two", "three")
        self.fileListOptionMenu.place(x=20, y=90)
        self.populate_file_list()
        
        processButton = Button(self, text="Process",
            command=self.process, width=14)
        processButton.place(x=20, y=130)


        viewResultsButton = Button(self, text="...",
            command=self.view_process_image, width=6)
        viewResultsButton.place(x=120, y=130)

        lowMagButton = Button(self, text="Low Mag",
            command=self.process_low_mag, width=12)
        lowMagButton.place(x=20, y=250)

        spotFinderButton = Button(self, text="Spot Finder",
            command=self.spotfind_low_mag, width=12)
        spotFinderButton.place(x=20, y=280)
        
        # close buttons
        closeButton = Button(self, text="Close",
            command=self.close_window, width=14)
        closeButton.place(x=20, y=350)

        ## 2nd column

    def populate_file_list(self):
        dirs = self.get_filepaths(r"..\data")
        lista = []
        for f in dirs:
            if f.endswith(".png"):
                lista.append(f)
        if len(lista) == 0:
            lista.append("none.png")
        self.fileListVariable.set(lista[0])
        self.cur_fn = lista[0]
        self.fileListOptionMenu['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        new_choices = ('a', 'b', 'c')
        for choice in lista:
            self.fileListOptionMenu['menu'].add_command(label=choice,
                                                        command=lambda item=choice: self.callback(item))
    def callback(self,item): 
        self.fileListOptionMenu.configure(text=item)
        self.fileListVariable.set(item)
        self.cur_fn = item

    def view_process_image(self):
        wimg = NGA_WImage()
        wimg.load(r"../resources/matlab/process.png")
        
    def dummy(self):
        self.processResult.configure(background=self.sys.win_cfg.cGood, text="Processed")

    def not_dummy(self):
        self.processResult.configure(background=self.sys.win_cfg.cBad, text="Processing")
        self.countResult.configure(background=self.sys.win_cfg.cUnknown, text=str(0))
        self.extraInfoResult.configure(background=self.sys.win_cfg.cUnknown, text="")
        self.update()
    def process(self):
        self.not_dummy()
        print self.cur_fn
        data = self.process.process_file(r"../resources/matlab/" + str(self.cur_fn))
        #self.dummy()
        self.processResult.configure(background=self.sys.win_cfg.cGood, text=("{0:.2f} (s)".format(data['run_time'])))
        self.countResult.configure(background=self.sys.win_cfg.cGood, text=str(data['particles']))
        extraInfoText = "Kpts: {0}, Kt: {1:.2f} (s)".format(data['keypoints'], data['key_run_time'])
        self.extraInfoResult.configure(background=self.sys.win_cfg.cUnknown, text=extraInfoText)
    def process_low_mag(self):
        lowmag = NGA_Interface_IRIS()
        lowmag.load(r"../resources/matlab/chip7_postDataSet1622571.png")
    def spotfind_low_mag(self):
        lowmag = NGA_Interface_IRIS()
        lowmag.remove_sr(r"../resources/matlab/contours_spot.png")
        lowmag.spot(r"../resources/matlab/contours_spot.png")

        lowmag = NGA_Interface_IRIS()
        lowmag.spot(r"../resources/matlab/contours_spot2.png")
        #lowmag.spot(r"../resources/matlab/spots3.png")
    def incorporate_py_config(self):
        print "Inc!"
        #for key in self.cam.cam_config.defaults.config:
            #if (key == "gaussian"):
                #self.cam.cam_config.defaults.config['shutter'] = self.sys.py_cfg.defaults.config['shutter']
            #if (key == "contrast"):
                # frames is special, it's value was stored and will overwrite in
                # NGA_Interface_Camera
                #self.cam.cam_config.defaults.config['frames'] = self.sys.py_cfg.defaults.config['frames']
                #self.cam.frms = self.sys.py_cfg.defaults.config['frames']
    def close_window(self):
        self.parent.destroy()
    

    def get_filepaths(self,directory):
        """This function will generate the file names in a directory 
        tree by walking the tree either top-down or bottom-up. For each 
        directory in the tree rooted at directory top (including top itself), 
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """

        file_paths = []  # List which will store all of the full filepaths.

        # Walk the tree.
        for root, directories, files in os.walk(directory):

            for filename in files:

                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)

                file_paths.append(filename)  # Add it to the list.

        return file_paths  # Self-explanatory.
