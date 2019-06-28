# import sys
#
# def trace_func(frame, event, arg):
#     print 'Context: ', frame.f_code.co_name, '\tFile:', frame.f_code.co_filename, '\tLine:', frame.f_lineno, '\tEvent:', event
#     return trace_func
#
# sys.settrace(trace_func)

from Tkinter import Tk, Label, Toplevel, BOTH
from ttk import Frame, Button, Style
from PIL import Image, ImageTk

from NGA_Config.Window import NGA_Config_Window

from NGA_Window.LED import NGA_Window_LED
from NGA_Window.Camera import NGA_Window_Camera
from NGA_Window.Config import NGA_Window_Config
from NGA_Window.Stage import NGA_Window_Stage
from NGA_Window.Process import NGA_Window_Process
from NGA_Window.Focus import NGA_Window_Focus
from NGA_Window.Pneumatics import NGA_Window_Pneumatics
from NGA_Window.Testing import NGA_Window_Testing
from NGA_Window.LowMag import NGA_Window_LowMag

from NGA_Window.FileInfo import NGA_Window_FileInfo

from NGA_Sys.Sys import NGA_Sys


class IRIS(Frame):


    sys = None
    load_other_w = True
    
    enable_panel_config = True
    enable_panel_led = True
    enable_panel_camera = True
    enable_panel_stage = True
    enable_panel_file = False
    enable_panel_process = False
    enable_panel_focus = True
    enable_panel_pneumatics = False
    enable_panel_testing = False
    enable_panel_lowmag = True

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.sys = NGA_Sys()
        self.sys.c_main_window = self

        self.initUI()

    def initUI(self):

        #self.parent.title("SP-IRIS Main")
        self.parent.iconbitmap(default=r"../resources/nga.ico")
        self.style = Style().configure("TFrame", background="#FFFFFF")
        #self.style.theme_use("default")

        bard = Image.open(r"../resources/nexgen_logo_80.png")
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(self, image=bardejov)
        label1.image = bardejov
        label1.place(x=20, y=20)

        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit",
            command=self.endProgram, width=12)
        quitButton.place(x=20, y=140)

        if (self.enable_panel_config):
            configButton = Button(self, text="Config Panel",
                                  command=self.panel_config, width=15)
            configButton.place(x=150, y=20)

        if (self.enable_panel_led):
            ledButton = Button(self, text="LED Panel",
                               command=self.panel_led, width=15)
            ledButton.place(x=150, y=60)

        if (self.enable_panel_camera):
            camButton = Button(self, text="Camera Panel",
                               command=self.panel_cam, width=15)
            camButton.place(x=150, y=100)

        if (self.enable_panel_stage):
            stageButton = Button(self, text="Stage Panel",
                               command=self.panel_stage, width=15)
            stageButton.place(x=150, y=140)

        if (self.enable_panel_file):
            ## 2nd column
            fileinfoButton = Button(self, text="File Panel",
                               command=self.panel_fileinfo, width=16)
            fileinfoButton.place(x=270, y=20)

        if (self.enable_panel_process):
            processButton = Button(self, text="Process Panel",
                               command=self.panel_process, width=16)
            processButton.place(x=270, y=60)

        if (self.enable_panel_focus):
            focusButton = Button(self, text="Focus Panel",
                               command=self.panel_focus, width=16)
            focusButton.place(x=270, y=100)
        if (self.enable_panel_pneumatics):
            pneumaticsButton = Button(self, text="Pneumatics Panel",
                               command=self.panel_pneumatics, width=16)
            pneumaticsButton.place(x=270, y=140)

        if(self.enable_panel_lowmag):
            lowmagButton = Button(self, text="Low Mag Panel",
                                command=self.panel_lowmag, width=16)
            lowmagButton.place(x=270, y=20)


        # Config Panel
        if (self.enable_panel_config):
            self.w_Config = Toplevel(self.parent)
            self.c_Config = NGA_Window_Config(self.w_Config, self.sys)

        # LED Panel
        if (self.enable_panel_led):
            self.w_LED = Toplevel(self.parent)
            self.c_LED = NGA_Window_LED(self.w_LED, self.sys)

        # Camera Panel
        if (self.enable_panel_camera):
            self.w_Cam = Toplevel(self.parent)
            self.c_Cam = NGA_Window_Camera(self.w_Cam, self.sys)

        # Stage Panel
        if (self.enable_panel_stage):
            self.w_Stage = Toplevel(self.parent)
            self.c_Stage = NGA_Window_Stage(self.w_Stage, self.sys)

        # FileInfo Panel
        if (self.enable_panel_file):
            self.w_Fileinfo = Toplevel(self.parent)
            self.c_Fileinfo = NGA_Window_FileInfo(self.w_Fileinfo, self.sys)

        # Process Panel
        if (self.enable_panel_process):
            self.w_Process = Toplevel(self.parent)
            self.c_Process = NGA_Window_Process(self.w_Process, self.sys)

        # Focus Panel
        if (self.enable_panel_focus):
            self.w_Focus = Toplevel(self.parent)
            self.c_Focus = NGA_Window_Focus(self.w_Focus, self.sys)

        # Pneumatics Panel
        if (self.enable_panel_pneumatics):
            self.w_Pneumatics = Toplevel(self.parent)
            self.c_Pneumatics = NGA_Window_Pneumatics(self.w_Pneumatics, self.sys)

        # Testing Panel
        if (self.enable_panel_testing):
            self.w_Testing = Toplevel(self.parent)
            self.c_Testing = NGA_Window_Testing(self.w_Testing, self.sys)

        #Low Mag Panel
        if (self.enable_panel_lowmag):
            self.w_LowMag = Toplevel(self.parent)
            self.c_LowMag = NGA_Window_LowMag(self.w_LowMag, self.sys)



        if (self.load_other_w == False):
            if (self.enable_panel_config):
                self.c_Config.close_window()
            if (self.enable_panel_led):
                self.c_LED.close_window()
            if (self.enable_panel_camera):
                self.c_Cam.close_window()
            if (self.enable_panel_stage):
                self.c_Stage.close_window()
            if (self.enable_panel_file):
                self.c_Fileinfo.close_window()
            if (self.enable_panel_process):
                self.c_Process.close_window()
            if (self.enable_panel_focus):
                self.c_Focus.close_window()
            if (self.enable_panel_pneuamtics):
                self.c_Pneumatics.close_window()

    def endProgram(self):
        self.c_Cam.quitDaemon()
        self.parent.destroy()

    def panel_led(self):
        if (self.c_LED.winfo_exists() == 1): #window exists
        #close window
            self.c_LED.close_window()
        else: #open window
            self.w_LED = Toplevel(self.parent)
            self.c_LED = NGA_Window_LED(self.w_LED, self.sys)

    def panel_cam(self):
        if (self.c_Cam.winfo_exists() == 1): #window exists
        #close window
            self.c_Cam.close_window()
        else: #open window
            self.w_Cam = Toplevel(self.parent)
            self.c_Cam = NGA_Window_Camera(self.w_Cam, self.sys)

    def panel_config(self):
        if (self.c_Config.winfo_exists() == 1): #window exists
        #close window
            self.c_Config.close_window()
        else: #open window
            self.w_Config = Toplevel(self.parent)
            self.c_Config = NGA_Window_Config(self.w_Config, self.sys)
    def panel_stage(self):
        if (self.c_Stage.winfo_exists() == 1): #window exists
        #close window
            self.c_Stage.close_window()
        else: #open window
            self.w_Stage = Toplevel(self.parent)
            self.c_Stage = NGA_Window_Stage(self.w_Stage, self.sys)
    def panel_process(self):
        if (self.c_Process.winfo_exists() == 1): #window exists
        #close window
            self.c_Process.close_window()
        else: #open window
            self.w_Process = Toplevel(self.parent)
            self.c_Process = NGA_Window_Process(self.w_Process, self.sys)
    def panel_fileinfo(self):
        if (self.c_Fileinfo.winfo_exists() == 1): #window exists
        #close window
            self.c_Fileinfo.close_window()
        else: #open window
            self.w_Fileinfo = Toplevel(self.parent)
            self.c_Fileinfo = NGA_Window_FileInfo(self.w_Fileinfo, self.sys)
    def panel_focus(self):
        if (self.c_Focus.winfo_exists() == 1): #window exists
        #close window
            self.c_Focus.close_window()
        else: #open window
            self.w_Focus = Toplevel(self.parent)
            self.c_Focus = NGA_Window_Focus(self.w_Focus, self.sys)
    def panel_pneumatics(self):
        if (self.c_Pneumatics.winfo_exists() == 1): #window exists
        #close window
            self.c_Pneumatics.close_window()
        else: #open window
            self.w_Pneumatics = Toplevel(self.parent)
            self.c_Pneumatics = NGA_Window_Pneumatics(self.w_Pneumatics, self.sys)

    def panel_lowmag(self):
        if (self.c_LowMag.winfo_exists() == 1):
        #close window
            self.c_LowMag.close_window()
        else:
            self.w_LowMag = Toplevel(self.parent)
            self.c_LowMag = NGA_Window_LowMag(self.w_LowMag, self.sys)

    def close_leds(self):
        if (self.c_LED.winfo_exists() == 1): #window exists
            self.c_LED.close_window()

    def reload_leds(self):
        if (self.c_LED.winfo_exists() == 1): #window exists
            self.c_LED.close_window()
            self.w_LED = Toplevel(self.parent)
            self.c_LED = NGA_Window_LED(self.w_LED, self.sys)

    def close_stages(self):
        if (self.c_Stage.winfo_exists() == 1): #window exists
            self.c_Stage.close_window()

    def reload_stages(self):
        if (self.c_Stage.winfo_exists() == 1): #window exists
            self.c_Stage.close_window()
            self.w_Stage = Toplevel(self.parent)
            self.c_Stage = NGA_Window_Stage(self.w_Stage, self.sys)


def main():

    cfg = NGA_Config_Window()

    root = Tk()
    root.geometry(cfg.wMain)
    root.title(cfg.sMain)

    app = IRIS(root)
    root.mainloop()






if __name__ == '__main__':
    main()
