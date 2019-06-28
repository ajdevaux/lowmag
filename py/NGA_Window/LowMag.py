from __future__ import division
from Tkinter import *
import tkMessageBox
from ttk import Frame, Button, Style
import os.path
from datetime import date, datetime
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
import pylab
import numpy
import time
import array

from shutil import copyfile
import png

from NGA_Window.Camera import NGA_Window_Camera
from NGA_Interface.LED import NGA_Interface_LED
from numpy.ma.bench import zs

class NGA_Window_LowMag(Frame):


    #homePos = [-10,0,2]
    homePos = [0,0,0]
    
    scanMirror = [2.3,-20,0] #for Dry

    options = [
        "NSF AIR - 90nm",
        "NV16 - 30nm",
        "NV10 - 90nm",
        "NV10B - 60nm",
        "NV16B - 60nm",
        "NV16B (dry) - 60nm"
    ]
    # Chip Modes: (*** note: ask Dave to make cooler chip names ***)
    #   1. NSF AIR - 90nm
    #   2. NV16 - 30nm
    #   3. NV10 - 90nm
    #   4. NV10B - 60nm
    #   5. NV16B - 60nm

    zoff = 0 #when stages are misaligned
    scanNSFAIR_1 = [-0.5,-18.1,-1+zoff]
    scanNSFAIR_2 = [-0.5,-18.1,-1+zoff]
    scanNV16_1 = [1.1,-18.1,-1+zoff] 
    scanNV16_2 = [1.1,-18.1,-1+zoff]
    scanNV10_1 = [2.3,-20,0+zoff] 
    scanNV10_2 = [2.3,-20,0+zoff] 
    scanNV10B_1 = [2.3,-20,0+zoff] 
    scanNV10B_2 = [2.3,-20,0+zoff] 
    scanNV16B_1 = [4.5,-20,0+zoff] 
    scanNV16B_2 = [4.5,-20,0+zoff]

    # Old modes commented out rather than deleted, for sanity.
    #scan90_1 = [1.0,-13.6,-1.4-1.8] #for Dry
    #scan90_2 = [1.0,-13.6,-1.85-1.8] #for Dry
    #scan60_1 = [1.0,-13.6,-1.2-1.8] #for Dry
    #scan60_2 = [1.0,-13.6,-1.85-1.8] #for Dry
    #scan30_1 = [2.6,-13.6,-1.4-1.8] #for Liquid
    #scan30_2 = [2.6,-13.6,-1.85-1.8] #for Liquid
    #scan60Long_1 = [4.0,-13.6,-1.2-1.8] #for Dry Long
    #scan60Long_2 = [4.0,-13.6,-1.85-1.8] #for Dry Long
     

    def __init__(self,parent,sys):
        Frame.__init__(self,parent)

        self.parent = parent
        self.sys = sys

        self.sys.c_lowmag = self

        self.parent.geometry(self.sys.win_cfg.wLowMag)
        self.parent.title(self.sys.win_cfg.sLowMag)
        
        self.sys.c_cam.setup_camera()
        self.sys.c_led.led_serial_status()
        if(self.sys.c_led.status == ":0"):
                self.sys.c_stage.home_stages()
                        
        self.longchip = 0
        
        self.initUI()

    def initUI(self):

        self.style = Style().configure("TFrame", background=self.sys.win_cfg.cBackground)
        self.pack(fill=BOTH, expand=1)

        titleLabel = Label(self, text=self.sys.win_cfg.sLowMag,
                            background="light blue",
                            width=15, height=1)
        titleLabel.place(x=5, y=5)

        prefixLabel= Label(self, text="File Prefix",
                                   background = self.sys.win_cfg.cBackground,width=9, height=1)
        prefixLabel.place(x=5, y=60)

        self.prefixEntry = Entry(self, width=30,background=self.sys.win_cfg.cTextBackground)
        self.prefixEntry.place(x=10, y=85)

        self.prefixEntry.insert(0,"CHIP")

        numberLabel= Label(self, text="Chip #",
                                   background = self.sys.win_cfg.cBackground,width=9, height=1)
        numberLabel.place(x=5, y=110)

        self.numberEntry = Entry(self, width=10,
                                         justify="center",background=self.sys.win_cfg.cTextBackground)
        self.numberEntry.place(x=10, y=135)

        self.numberEntry.insert(0,"1")
        
        if (self.checkIm(str(1)) == True):
            self.numberEntry.config(background="green")
        else:
            self.numberEntry.config(background="red")

        self.numDownButton = Button(self, text="prev",command=self.numDown, width=5)
        self.numDownButton.place(x=80, y=120)

        self.numUpButton = Button(self, text="next",command=self.numUp, width=5)
        self.numUpButton.place(x=80, y=145)

        self.deleteButton = Button(self, text="Delete",command=self.deleteIm, width = 10)
        self.deleteButton.place(x=125, y = 130)

        #self.stitchButton = Button(self, text="Stitch",command=self.stitch, width = 10)
        #self.stitchButton.place(x=125, y = 5)

        

        

        self.acquireButton = Button(self, text="Acquire",command=self.acquire, width = 20)
        self.acquireButton.place(x=5,y=180)

        self.mirrorButton = Button(self, text="Mirror",command=self.mirrorBtn, width = 5)
        self.mirrorButton.place(x=150,y=180)

        self.loadButton = Button(self, text="Unload",command=self.unload, width = 8)
        self.loadButton.place(x=130, y=30)   
        self.autoUnload = IntVar()
        self.autoUnload.set(1)

        self.autoUnloadCheck = Checkbutton(self, text = "Auto-Unload", variable = self.autoUnload, \
                                            onvalue = 1, offvalue = 0, height=1, \
                                            width = 10)
        self.autoUnloadCheck.place(x=90, y=60)

        self.v = IntVar()

        self.v.set(0)

        # Setting up the option box for the chip version
        self.chipMode = StringVar()
        self.chipMode.set(self.options[3]) # Default value
        self.chipSelect = OptionMenu(self,self.chipMode,*self.options)
        self.chipSelect.place(x=5, y=30)
        
        #self.modeDryV2 = Radiobutton(self, text="60", variable=self.v, value=0)
        #self.modeDryV2.place(x=5, y=30)
        #self.modeDry = Radiobutton(self, text="90", variable=self.v, value=1)
        #self.modeDry.place(x=45, y=30)
        #self.modeWet = Radiobutton(self, text="30", variable=self.v, value=2)
        #self.modeWet.place(x=85, y=30)

        #self.longCheck = Radiobutton(self, text="60-Long", variable=self.v, value=3)
        #self.longCheck.place(x=125, y = 5)

    def numUp(self):
        num = self.numberEntry.get()
        num = str(int(num)+1);
        self.numberEntry.delete(0, END)
        self.numberEntry.insert(0,str(int(num)))
        if (self.checkIm(num) == True):
            self.numberEntry.config(background="green")
        else:
            self.numberEntry.config(background="red")


    def numDown(self):
        num = self.numberEntry.get()
        if(int(num) > 1):
            num = str(int(num)-1);
            self.numberEntry.delete(0, END)
            self.numberEntry.insert(0,str(int(num)))
            if (self.checkIm(num) == True):
                self.numberEntry.config(background="green")
            else:
                self.numberEntry.config(background="red")


    def deleteIm(self):
            today = date.today()
            todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"
            todaystr = time.strftime("%Y-%m-%d") + "/"
            prefix = self.prefixEntry.get() + "_"
            num = self.numberEntry.get()
            os.remove("../data/" + todaystr + prefix + num.zfill(3)+"_1.png") 
            os.remove("../data/" + todaystr + prefix + num.zfill(3)+"_2.png")
            if (self.checkIm(num) == True):
                    self.numberEntry.config(background="green")
            else:
                    self.numberEntry.config(background="red")

    def mirrorBtn(self):
        self.mirror()
        #self.focus()
        
    def dataMirrorFiles(self):
        runMore = 0
        mirror_exists = self.mirror_exists()
        if (mirror_exists == False ):
            proceed = self.checkMirrorFiles()
            if (proceed == 0): #mirror is not old
                self.mirror_copy()
                runMore = 1
            elif (proceed == 1): # take new mirror
                runMore = 0
            elif (proceed == 2): #use old mirror
                self.mirror_copy()
                runMore = 1
        else:
            runMore = 1
        return runMore
            
    def checkMirrorFiles(self):
        proceed = 0
        mirror_fn1 = "../data/mirror/MIRROR_01.png"
        mirror_fn2 = "../data/mirror/MIRROR_02.png"
        
        mir_fold = "../data/mirror/"

        
        mirror_date = time.strftime("%Y-%m-%d",time.gmtime(os.path.getmtime(mirror_fn1)))
        days_since = self.days_between(mirror_date,time.strftime("%Y-%m-%d",time.gmtime()))
        if (days_since > 6):
            result = tkMessageBox.askyesno("Mirror File","It has been %d days since you took a mirror, would you like to take a new mirror before scanning?" % days_since)
            if (result == True):
                proceed = 1 #"Take new mirror"
            else:
                proceed = 2 #"Use existing mirror"
            
        return proceed
    
    def days_between(self,d1, d2):
        d1b = datetime.strptime(d1, "%Y-%m-%d")
        d2b = datetime.strptime(d2, "%Y-%m-%d") 
        return abs((d2b - d1b).days)
    
    def focus(self, focus_point = 1, led_color = 1):
            '''
            mode = self.v.get() 
            if(mode == 2): #30 nm
                if (led_color == 1):
                    scanPos = self.scan30_1
                elif (led_color == 2):
                    scanPos = self.scan30_2
            elif(mode == 1): #90 nm
                if (led_color == 1):
                    scanPos = self.scan90_1
                elif (led_color == 2):
                    scanPos = self.scan90_2
            elif(mode == 0): #30 nm
                if (led_color == 1):
                    scanPos = self.scan60_1
                elif (led_color == 2):
                    scanPos = self.scan60_2        
            elif(mode == 3): #60 long
                if (led_color == 1):
                    scanPos = self.scan60Long_1
                elif (led_color == 2):
                    scanPos = self.scan60Long_2             
            '''
            mode = self.chipMode.get()
            if(mode == self.options[0]):
                if(led_color == 1):
                    scanPos = self.scanNSFAIR_1
                elif(led_color == 2):
                    scanPos = self.scanNSFAIR_2
            elif(mode == self.options[1]):
                if(led_color == 1):
                    scanPos = self.scanNV16_1
                elif(led_color == 2):
                    scanPos = self.scanNV16_2
            elif(mode == self.options[2]):
                if(led_color == 1):
                    scanPos = self.scanNV10_1
                elif(led_color == 2):
                    scanPos = self.scanNV10_2
            elif(mode == self.options[3]):
                if(led_color == 1):
                    scanPos = self.scanNV10B_1
                elif(led_color == 2):
                    scanPos = self.scanNV10B_2
            elif(mode == self.options[4]):
                if(led_color == 1):
                    scanPos = self.scanNV16B_1
                elif(led_color == 2):
                    scanPos = self.scanNV16B_2
            elif(mode == self.options[5]):
                if(led_color == 1):
                    scanPos = self.scanNV16B_1
                elif(led_color == 2):
                    scanPos = self.scanNV16B_2
            
            
            self.sys.c_cam.close_realtime()
            oldfrms = self.sys.hw.cam.frms
            self.sys.hw.cam.frms = str(1)
            scores = []
            zpos = []
            for x in range(-50, 30, 5):
                offsetval = x/100
                self.sys.hw.stg.move_z(scanPos[2]+offsetval)
                z_status = self.sys.hw.stg.status_z()
                while ( (z_status['axis_moving'] == True)):
                    time.sleep(0.05)
                    z_status = self.sys.hw.stg.status_z()
                self.sys.hw.cam.dog_image(1)
                scores.append(float(self.sys.hw.cam.dog_score))
                #print scanPos[2]+offsetval
                zpos.append(scanPos[2]+offsetval)
            
            self.sys.hw.cam.frms = oldfrms
            
            # set focus to max change of slope
            y = numpy.gradient(scores)
            zs = numpy.argmax(y)
            zs2 = numpy.argmax(scores)
            zsmin = numpy.argmin(scores)
            
            if (focus_point == 0): # middle of slope
                focus_z = zs
            elif (focus_point == 1): #max of score
                focus_z = zs2
            elif (focus_point == 2): #min of score
                focus_z = zsmin
                    
            if (0):
                plt.interactive(True) #need to add this or program freezes while plotting
                plt.plot(zpos,scores)
                plt.show()               
                fig2 = plt.figure()
                zero_crossings = numpy.where(numpy.diff(numpy.sign(y)))[0]
                #print zero_crossings
                plt.plot(zpos,y)
                plt.plot(zpos[focus_z],y[focus_z],'gx')
                plt.show()
            
            ## move to z
            print(zpos[focus_z])
            print "Focus: " + str(focus_point)  + " - " + str(zpos[focus_z])
            self.sys.hw.stg.move_z(zpos[focus_z])
            z_status = self.sys.hw.stg.status_z()
            while ( (z_status['axis_moving'] == True)):
                time.sleep(0.05)
                z_status = self.sys.hw.stg.status_z()
            
            
    def moveAndCheck(self, x, y):
        self.sys.hw.stg.move_x(x)
        self.sys.hw.stg.move_y(y)
        x_status = self.sys.hw.stg.status_x()
        while ( (x_status['axis_moving'] == True)):
                time.sleep(0.05)
                x_status = self.sys.hw.stg.status_x()
        
        y_status = self.sys.hw.stg.status_y()
        while ( (y_status['axis_moving'] == True)):
                time.sleep(0.05)
                y_status = self.sys.hw.stg.status_y()
                
    def read_pgm(self, filename, byteorder='>'):
        #"""Return image data from a raw PGM file as numpy array.
    #
     #   Format specification: http://netpbm.sourceforge.net/doc/pgm.html
    

        with open(filename, 'rb') as f:
            buffer = f.read()
        try:
            header, width, height, maxval = re.search(
                b"(^P5\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n])*"
                b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
        except AttributeError:
            raise ValueError("Not a raw PGM file: '%s'" % filename)
        return numpy.frombuffer(buffer,
                                dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                                count=int(width)*int(height),
                                offset=len(header)
                                ).reshape((int(height), int(width)))
                                       
    def mirror(self):
        start_time = time.time()
        self.mirror1()
        self.mirror2()
        self.mirror_copy()
        elapsed_time = time.time() - start_time
        str_cap = "Mirror Time: {0:.2f} s.".format(elapsed_time)
        print str_cap
    
    def mirror2(self):
            self.disableButtons()
            
            #self.backup_mirror() #make copy of mirror before replacing
            
            today = date.today()
            #todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"\\"
            folder = "../data/mirror/" # + todaystr
            image = []
            for i in range(0,9):
                fn1 = folder + "MIRROR_01_" + str(i) + ".pgm"
                image.append(self.read_pgm(fn1, byteorder='>'))
                os.remove(fn1)
                #plt.imshow(image)
                #plt.show()
                
            #d = numpy.array([image[0],image[1],image[2],image[3],image[4],image[5],image[6],image[7],image[8]])
            e = numpy.median(image, axis=0)
   
            fn1 = folder + "MIRROR_01" + ".png"
            f = open(fn1, 'wb')      # binary mode is important
            w = png.Writer(len(e[0]), len(e), greyscale=True, bitdepth=16)
            w.write(f, e)
            f.close()
            
            image = []
            for i in range(0,9):
                fn2 = folder + "MIRROR_02_" + str(i) + ".pgm"
                image.append(self.read_pgm(fn2, byteorder='>'))
                os.remove(fn2)
                #plt.imshow(image)
                #plt.show()
                
            #d = numpy.array([image[0],image[1],image[2],image[3],image[4],image[5],image[6],image[7],image[8]])
            e = numpy.median(image, axis=0)
   
            fn2 = folder + "MIRROR_02" + ".png"
            f = open(fn2, 'wb')      # binary mode is important
            w = png.Writer(len(e[0]), len(e), greyscale=True, bitdepth=16)
            w.write(f, e)
            f.close()
            self.enableButtons()
#             if (len(filename2) > 0):
#                 imgA = mpimg.imread(filename2,cv2.IMREAD_GRAYSCALE)
#                 img2A = cv2.resize(imgA, (0,0), fx=0.5, fy=0.5)
#                 heightA, width1A, channelsA = img2A.shape
#                 
#                 blue_image = img2A[:,:,1]
#                 red_image = img2[:,:,1]
#                     
#                 blank_image = 255*numpy.ones((height,width1,3), numpy.uint8)
#                 blank_image[:,:,0] = blank_image[:,:,0]-red_image
#                 blank_image[:,:,2] = blank_image[:,:,2]-blue_image
# 
#                 plt.imshow(blank_image)

    def backup_mirror(self):
        mir_fold = "../data/mirror/"
        
        og_fn1 = mir_fold + "MIRROR_01" + ".png"
        og_fn2 = mir_fold + "MIRROR_02" + ".png"
        
        mirror_date = time.strftime("%Y-%m-%d",time.gmtime(os.path.getmtime(og_fn1)))

        folder = "../data/mirror/" + mirror_date + "/"
        fn1 = folder + "MIRROR_01" + ".png"
        fn2 = folder + "MIRROR_02" + ".png"
        
        if(os.path.isdir(folder) == False):
                os.mkdir(folder)
        
        copyfile(og_fn1, fn1)
        copyfile(og_fn2, fn2)
        os.remove(og_fn1)
        os.remove(og_fn2)
        
    def mirror_exists(self):
        today = date.today()        
        todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"
        todaystr = time.strftime("%Y-%m-%d") + "/"
        folder = "../data/" + todaystr
        fn1 = folder + "MIRROR_01" + ".png"
        fn2 = folder + "MIRROR_02" + ".png"
        
        file1 = os.path.isfile(fn1)
        file2 = os.path.isfile(fn2) 
        
        return (file1 and file2)
        
    def mirror_copy(self): #copy mirror to data folder
        today = date.today()
        todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"

        todaystr = time.strftime("%Y-%m-%d") + "/"
        folder = "../data/" + todaystr
        fn1 = folder + "MIRROR_01" + ".png"
        fn2 = folder + "MIRROR_02" + ".png"
        
        mir_fold = "../data/mirror/"
        
        if(os.path.isdir(folder) == False):
                os.mkdir(folder)
        
        og_fn1 = mir_fold + "MIRROR_01" + ".png"
        og_fn2 = mir_fold + "MIRROR_02" + ".png"
        
        copyfile(og_fn1, fn1)
        copyfile(og_fn2, fn2)
        
    def mirror1(self):
            
            self.load()
            self.disableButtons()
            today = date.today()
            #todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"\\"
            folder = "../data/mirror/" # + todaystr
            if(os.path.isdir(folder) == False):
                os.mkdir(folder)
            #self.sys.c_cam.close_realtime()

            xoffsets = [-0.512, -0.512, -0.512, 0, 0, 0, 0.512, 0.512, 0.512]
            yoffsets = [-0.512, 0, 0.512, -0.512, 0, 0.5, -0.512, 0, 0.512]
            
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            self.focus(1) #max peak
            
            for i in range(0,9):
                xpos = self.scanMirror[0] + xoffsets[i]
                ypos = self.scanMirror[1] + yoffsets[i]
                self.moveAndCheck(xpos, ypos)
                fn1 = folder + "MIRROR_01_" + str(i)
                self.sys.hw.cam.fn = fn1
                self.sys.hw.cam.imagePGM()
                
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED2_ON)
            self.focus(1) #max peak
            
            for i in range(0,9):
                xpos = self.scanMirror[0] + xoffsets[i]
                ypos = self.scanMirror[1] + yoffsets[i]
                self.moveAndCheck(xpos, ypos)
                fn2 = folder + "MIRROR_02_" + str(i)
                self.sys.hw.cam.fn = fn2
                self.sys.hw.cam.imagePGM()
            
    
            self.enableButtons()
            
            aunload = self.autoUnload.get()

            if (aunload > 0):
                self.unload()  
            
            
    def acquire(self):
        run = self.dataMirrorFiles() #check for mirror first
        if (run == 1):
            self.acquire_data() #acquire data
        
    def acquire_data(self):
            #mode = self.v.get()
            mode = self.chipMode.get()
            start_time = time.time()
            self.load()
            self.disableButtons()
            today = date.today()
            todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"
            todaystr = time.strftime("%Y-%m-%d") + "/"
            folder = "../data/" + todaystr
            if(os.path.isdir(folder) == False):
                os.mkdir(folder)
            #self.sys.c_cam.close_realtime()
            
            num = self.numberEntry.get().zfill(3)
            
            ## LED1
            ledn = 1
            fn1 = folder + self.prefixEntry.get()+"_"+num + "_1"
            self.sys.hw.cam.fn = fn1
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)

            print("before focus 1. mode = " + mode)

            '''
            if (mode == 2): #30
                self.focus(1,ledn) #min score
            elif (mode == 1): #90
                self.focus(0,ledn) #max slope
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            '''
            if(mode == self.options[0]):
                self.focus(0,ledn)
            elif(mode == self.options[1]):
                self.focus(1,ledn)
            elif(mode == self.options[2]):
                self.focus(0,ledn)
            elif(mode == self.options[3]):
                self.focus(1,ledn)
            elif(mode == self.options[4]):
                self.focus(1,ledn)
            elif(mode == self.options[5]):
                self.focus(1,ledn)
            print('done with first focus')
            self.sys.hw.cam.image()
            print('done with first image')
            ## LED 2
            ledn = 2
            fn2 = folder + self.prefixEntry.get()+"_"+num + "_2"
            self.sys.hw.cam.fn = fn2
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED2_ON)
            '''
            if (mode == 2): #30
                self.focus(2,ledn) #min score
            elif (mode == 1): #90
                self.focus(1,ledn) #max score
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            '''
            print('before focus 2')
            if(mode == self.options[0]):
                self.focus(0,ledn)
            elif(mode == self.options[1]):
                self.focus(1,ledn)
            elif(mode == self.options[2]):
                self.focus(0,ledn)
            elif(mode == self.options[3]):
                self.focus(1,ledn)
            elif(mode == self.options[4]):
                self.focus(1,ledn)
            elif(mode == self.options[5]):
                self.focus(1,ledn)                
            print('second focus complete')
            
            self.sys.hw.cam.image()
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            if (self.checkIm(num) == True):
                    self.numberEntry.config(background="green")
            else:
                    self.numberEntry.config(background="red")
            self.showimhist(fn1+".png", fn2+".png")
            self.enableButtons()
            
            aunload = self.autoUnload.get()

            if (aunload > 0):
                self.unload()
                
            self.numUp()    
            
            elapsed_time = time.time() - start_time
            str_cap = "Capture Time: {0:.2f} s.".format(elapsed_time)
            print str_cap

            # Editing the first pixel
            print('about to edit pixel...')
            point = (0,0)

            reader = png.Reader(filename=fn1+'.png')
            w, h, pixels, metadata = reader.read_flat()

            ## set chip version in first pixel
            if(mode == self.options[0]):
                pixels[0] = 1
            elif(mode == self.options[1]):
                pixels[0] = 2
            elif(mode == self.options[2]):
                pixels[0] = 3
            elif(mode == self.options[3]):
                pixels[0] = 4
            elif(mode == self.options[4]):
                pixels[0] = 5
            elif(mode == self.options[5]):
                pixels[0] = 6
                
            output = open(fn1+'.png', 'wb')
            writer = png.Writer(w, h, **metadata)
            writer.write_array(output, pixels)
            output.close()
            print('done')
            
            #self.sys.c_cam.real_time()

    def stitch(self):
            # preserve old values
            old90_1 = self.scan90_1
            old90_2 = self.scan90_2
            old60_1 = self.scan60_1
            old60_2 = self.scan60_2
            old30_1 = self.scan30_1
            old30_2 = self.scan30_2

            # Offset the x
            self.scan90_1[0] -= 3
            self.scan90_2[0] -= 3
            self.scan60_1[0] -= 3
            self.scan60_2[0] -= 3
            self.scan30_1[0] -= 3
            self.scan30_2[0] -= 3
        
            mode = self.v.get()
            start_time = time.time()
            self.load()
            self.disableButtons()
            today = date.today()
            todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"
            todaystr = time.strftime("%Y-%m-%d") + "/"
            folder = "../data/" + todaystr
            if(os.path.isdir(folder) == False):
                os.mkdir(folder)
            #self.sys.c_cam.close_realtime()
            
            num = self.numberEntry.get().zfill(3)
            
            ## LED1
            ledn = 1
            fn1 = folder + self.prefixEntry.get()+"_"+num + "_1a"
            self.sys.hw.cam.fn = fn1
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            
            if (mode == 2): #30
                self.focus(1,ledn) #min score
            elif (mode == 1): #90
                self.focus(0,ledn) #max slope
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            self.sys.hw.cam.image()
            
            ## LED 2
            ledn = 2
            fn2 = folder + self.prefixEntry.get()+"_"+num + "_2a"
            self.sys.hw.cam.fn = fn2
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED2_ON)
            if (mode == 2): #30
                self.focus(2,ledn) #min score
            elif (mode == 1): #90
                self.focus(1,ledn) #max score
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            self.sys.hw.cam.image()
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            if (self.checkIm(num) == True):
                    self.numberEntry.config(background="green")
            else:
                    self.numberEntry.config(background="red")
            self.showimhist(fn1+".png", fn2+".png")
            self.enableButtons()
            


            ### MOVE THE STAGE
                        # Offset the x
            self.scan90_1[0] += 6
            self.scan90_2[0] += 6
            self.scan60_1[0] += 6
            self.scan60_2[0] += 6
            self.scan30_1[0] += 6
            self.scan30_2[0] += 6

            self.load()
            
            ## LED1
            ledn = 1
            fn1 = folder + self.prefixEntry.get()+"_"+num + "_1b"
            self.sys.hw.cam.fn = fn1
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            
            if (mode == 2): #30
                self.focus(1,ledn) #min score
            elif (mode == 1): #90
                self.focus(0,ledn) #max slope
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            self.sys.hw.cam.image()
            
            ## LED 2
            ledn = 2
            fn2 = folder + self.prefixEntry.get()+"_"+num + "_2b"
            self.sys.hw.cam.fn = fn2
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED2_ON)
            if (mode == 2): #30
                self.focus(2,ledn) #min score
            elif (mode == 1): #90
                self.focus(1,ledn) #max score
            elif (mode == 0): #60
                self.focus(1,ledn) #max score
            self.sys.hw.cam.image()
            self.sys.hw.led.command(NGA_Interface_LED.LED_OFF)
            self.sys.hw.led.command(NGA_Interface_LED.LED1_ON)
            if (self.checkIm(num) == True):
                    self.numberEntry.config(background="green")
            else:
                    self.numberEntry.config(background="red")
            self.showimhist(fn1+".png", fn2+".png")
            self.enableButtons()
            
            aunload = self.autoUnload.get()

            if (aunload > 0):
                self.unload()
                
            self.numUp()    
            
            elapsed_time = time.time() - start_time
            str_cap = "Capture Time: {0:.2f} s.".format(elapsed_time)
            print str_cap
            #self.sys.c_cam.real_time()

            # preserve old values
            #self.scan90_1 = old90_1
            #self.scan90_2 = old90_2
            #self.scan60_1 = old60_1
            #self.scan60_2 = old60_2
            #self.scan30_1 = old30_1
            #self.scan30_2 = old30_2
            self.scan90_1[0] -= 3
            self.scan90_2[0] -= 3
            self.scan60_1[0] -= 3
            self.scan60_2[0] -= 3
            self.scan30_1[0] -= 3
            self.scan30_2[0] -= 3


            

    def disableButtons(self):
            self.setButtons(DISABLED)

    def enableButtons(self):
            self.setButtons('normal')
    
    def setButtons(self,btnState):
            self.prefixEntry.config(state=btnState)
            self.numberEntry.config(state=btnState)
            self.numDownButton.config(state=btnState)
            self.numUpButton.config(state=btnState)
            self.deleteButton.config(state=btnState)
            self.acquireButton.config(state=btnState)
            self.loadButton.config(state=btnState)
            #self.modeDry.config(state=btnState)
            #self.modeWet.config(state=btnState)
            self.autoUnloadCheck.config(state=btnState)
            self.mirrorButton.config(state=btnState)
            
            
            #self.focusButton.config(state=DISABLED)
            self.parent.update()
        
    def checkIm(self, num):
        today = date.today()
        todaystr = str(today.year) +"-"+str(today.month) +"-"+str(today.day) +"/"
        todaystr = time.strftime("%Y-%m-%d") + "/"
        prefix = self.prefixEntry.get() + "_"
        return (os.path.isfile("../data/" + todaystr + prefix + num.zfill(3)+"_1.png") 
            & os.path.isfile("../data/" + todaystr + prefix + num.zfill(3)+"_2.png"))

    def load(self):
            self.disableButtons()
            self.loadButton["text"] = "Loading..."

            '''
                mode = self.v.get()
                if(mode == 2):
                    scanPos = self.scan30_1
                    #print str(scanPos[0])+" "+str(scanPos[1])+" "+str(scanPos[2])
                elif(mode == 1):
                    scanPos = self.scan90_1
                elif(mode == 0):
                    scanPos = self.scan60_1
                    #print str(scanPos[0])+" "+str(scanPos[1])+" "+str(scanPos[2])
                elif(mode==3):
                    scanPos = self.scan60Long_1
            '''
            
            mode = self.chipMode.get()
            print("Mode: " + mode)
            scanPos = [0, 0, 0]
            if(mode == self.options[0]):
               scanPos = self.scanNSFAIR_1
            elif(mode == self.options[1]):
               scanPos = self.scanNV16_1
            elif(mode == self.options[2]):
               scanPos = self.scanNV10_1
            elif(mode == self.options[3]):
               scanPos = self.scanNV10B_1
            elif(mode == self.options[4]):
               scanPos = self.scanNV16B_1
            elif(mode == self.options[5]):
               scanPos = self.scanNV16B_1
               
            print(scanPos)
            self.sys.hw.stg.move_z(scanPos[2])
            self.sys.c_stage.update_pos_x_y_z()
            self.sys.hw.stg.move_x(scanPos[0])
            self.sys.hw.stg.move_y(scanPos[1])
            self.sys.c_stage.update_pos_x_y_z()
            self.loadButton["text"] = "Unload"
            self.loadButton["command"] = self.unload
            self.enableButtons()

    def unload(self): 
            self.disableButtons()
            self.loadButton["text"] = "Unloading..."
            if self.sys.hw.led.led_on[0] == False:
                    self.sys.c_led.led_on()
            #self.sys.c_cam.real_time()
            self.sys.hw.stg.move_x(self.homePos[0])
            self.sys.hw.stg.move_y(self.homePos[1])
            self.sys.c_stage.update_pos_x_y_z()
            self.sys.hw.stg.move_z(self.homePos[2])
            self.sys.c_stage.update_pos_x_y_z()
            self.loadButton["text"] = "Load"
            self.loadButton["command"] = self.load
            self.enableButtons()

    def showimhist(self, filename, filename2 = ""):
            plt.interactive(True) #need to add this or program freezes while plotting
            #print filename
            img = mpimg.imread(filename,cv2.IMREAD_GRAYSCALE)
            img2 = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            height, width1, channels = img2.shape
            try:
                plt.close(0)
            except:
                pass #this will error out if window hasn't loaded yet, that's ok
            plt.figure(0)
            plt.imshow(img2)
            
#             if (len(filename2) > 0):
#                 imgA = mpimg.imread(filename2,cv2.IMREAD_GRAYSCALE)
#                 img2A = cv2.resize(imgA, (0,0), fx=0.5, fy=0.5)
#                 heightA, width1A, channelsA = img2A.shape
#                 
#                 blue_image = img2A[:,:,1]
#                 red_image = img2[:,:,1]
#                     
#                 blank_image = 255*numpy.ones((height,width1,3), numpy.uint8)
#                 blank_image[:,:,0] = blank_image[:,:,0]-red_image
#                 blank_image[:,:,2] = blank_image[:,:,2]-blue_image
# 
#                 plt.imshow(blank_image)
                
            hist = cv2.calcHist(img,[0],None,[256],[0,256])
            maxhist = max(hist)
            y = [((x/maxhist)*-1*height*.3) for x in hist]
            N = len(y)
            xold = range(N)
            x = [(x/(N-1))*width1 for x in xold]
            width = (1/N)*width1
            plt.bar(x, y, width, color="blue", bottom=height)
            plt.axis([0,width1,height,0])
            plt.title(filename)
            plt.show()


