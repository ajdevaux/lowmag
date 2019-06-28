import subprocess

# NGA CLASSES
from NGA_Utils.Text_Config_Save import NGA_Text_Config_Save
from NGA_Config.Camera import NGA_Config_Camera

class NGA_Interface_Camera:

    cam_detected = 0
    cam_error = False
    cam_config = None
    
    fn = ""
    fold = "..\\data\\"
    frms = 1
    bin = 1
    shutter = 25
    dog_score = 0

    extra_settings = ""

    
    config_file = r"..\config\config.cam.txt"
    
    def __init__(self,client):
        self.cam_config = NGA_Config_Camera()
        self.fn = self.fold + self.cam_config.defaults.config['filename']
        self.frms = self.cam_config.defaults.config['frames']
        self.bin = self.cam_config.defaults.config['bin']
        self.shutter = self.cam_config.defaults.config['shutter']
        self.client = client
        self.capture_mode = str(7);

    def image(self, mode=1, size=[0,0,0,0]):
        self.capture_mode = 7 #save PNG File
        if (mode == 1):
            self.fast_image()
        elif (mode == 2):
            self.roi_image(size)
            
    def imagePGM(self, mode=1, size=[0,0,0,0]):
        self.capture_mode = 1 #save PGM File
        if (mode == 1):
            self.fast_image()
        elif (mode == 2):
            self.roi_image(size)
            
    def clean_image(self):
        ### BUG HERE MUST CAPTURE A DUMMY FRAME FIRST WHEN MAKING CONFIGURATION CHANGES ###    # load defaults
        self.cam_config.defaults.config['filename'] = "temp_bug_image"
        self.cam_config.defaults.config['load_cam_config'] = 'true'
        self.cam_config.defaults.config['fps'] = str(80) #str(1000.0/float(self.cam_config.defaults.config['shutter']))
        # save camera properties
        NGA_Text_Config_Save(self.config_file,self.cam_config.defaults.config)
        self.flycap2_output = subprocess.check_output([self.camera_executable], shell=True)
        #self.fast_image()
        #Number of cameras detected: 0
        self.check_number_of_cameras()

    def check_number_of_cameras(self):
        self.cam_detected = 0
        self.cam_error = True
        lines = self.flycap2_output

        cam_d = 0
        for l in lines.split('\n'):
            if 'Number of cameras detected:' in l:
                tmp = l.split(":")
                tmp2 = tmp[1].strip()
                cam_d = int(tmp2)
        if (cam_d == 1):
            self.cam_detected = 1
            self.cam_error = False
        if (cam_d > 1):
            self.cam_detected = cam_d
            self.cam_error = True
            
    def dog_image(self, roi=0):
        self.cam_config.defaults.config['frames'] = self.frms
        self.cam_config.defaults.config['fps'] = str(80) #str(1000.0/float(self.cam_config.defaults.config['shutter']))

        sendString = "shutter:" + self.cam_config.defaults.config['shutter'] + ";wordsize:16;frames:" + self.frms + ";capture_mode:"+str(3)+";" + self.extra_settings
        
        if (roi == 1):
            sendString = sendString + "width:" + str(1920) + ";height:" + str(128) + ";top:" + str(536) + ";left:" + str(0) + ";\n" #+ "\n"
        else:
            sendString = sendString + "\n" 
                 
            
        #print sendString
    
        #clear settings string
        #self.client.connect()
        self.extra_settings = ""
        self.client.send(sendString)
        self.client.readDog()
        self.dog_score = self.client.dog_score
        #self.client.close()
        
    def fast_image(self):
        self.cam_config.defaults.config['filename'] = self.fn
        self.cam_config.defaults.config['frames'] = self.frms
        self.cam_config.defaults.config['fps'] = str(80) #str(1000.0/float(self.cam_config.defaults.config['shutter']))
        # save camera properties
        NGA_Text_Config_Save(self.config_file,self.cam_config.defaults.config)
        sendString = "shutter:" + self.cam_config.defaults.config['shutter'] + ";wordsize:16;filename:" + self.fn + ";frames:" + self.frms + ";capture_mode:"+str(self.capture_mode)+";extra_info:false;" + self.extra_settings + \
        "width:" + str(0) + ";height:" + str(0) + ";top:" + str(0) + ";left:" + str(0) + ";\n" #+ "\n""

        #print sendString
    
        #clear settings string
        #self.client.connect()
        self.extra_settings = ""
        self.client.send(sendString)
        self.client.readIm()
        #self.client.close()
        
    def quitCamera(self):
        sendString = "quit:1;" + "\n"
        self.client.send(sendString)
        #self.client.readIm()
        self.client.close()

    def roi_image(self, size):

        self.cam_config.defaults.config['filename'] = self.fn
        self.cam_config.defaults.config['frames'] = self.frms
        self.cam_config.defaults.config['fps'] = str(80) #str(1000.0/float(self.cam_config.defaults.config['shutter']))
        self.cam_config.defaults.config['width'] = str(size[0])
        self.cam_config.defaults.config['height'] = str(size[1])
        self.cam_config.defaults.config['top'] = str(size[2])
        self.cam_config.defaults.config['left'] = str(size[3])

        NGA_Text_Config_Save(self.config_file,self.cam_config.defaults.config)
        sendString = ("wordsize:16;filename:" + self.fn + ";frames:" + self.frms +
                      ";width:" + str(size[0]) + ";height:" +
                      str(size[1]) + ";top:" + str(size[2]) + ";left:" + str(size[3]) + ";\n")

        print sendString
        
        self.client.send(sendString)
        self.client.readIm()
        
        

        
        
        
