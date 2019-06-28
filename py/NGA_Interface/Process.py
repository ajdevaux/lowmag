import cv2
#from scipy import fftpack
#from PIL import Image, ImageTk
import numpy as np
#from matplotlib import pyplot as plt

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion

import subprocess

# NGA CLASSES
from NGA_Process.SP import NGA_Process_SP

class NGA_Interface_Process:

    img = None
    
    def __init__(self):
        self.img = None


    def process_file(self, fn):
        #a = subprocess.check_output("int_process.py " + fn, shell=True)
        #print a
        #data = self.get_stats(a)

        
        Process_SP = NGA_Process_SP(fn)
        prcs = Process_SP.process()
        data = self.get_stats2(prcs)
        
        return data

    def get_stats2(self, dic_vals):
        data = dict()

        data['particles'] = dic_vals['particles']
        data['run_time'] = dic_vals['delta_t']
        data['key_run_time'] = dic_vals['kp_t']
        data['keypoints'] = dic_vals['kp']
        return data

    def get_stats(self, lines):

        data = dict()
        particles = 0
        run_time = 0.0
        keypoints = 0
        key_run_time = 0.0
        for l in lines.split('\n'):
            if 'Particles Found:' in l:
                tmp = l.split(":")
                tmp2 = tmp[1].strip()
                particles = int(tmp2)
            if 'entire run time (s):' in l:
                tmp = l.split(":")
                tmp2 = tmp[1].strip()
                run_time = float(tmp2)
            if 'Keypoints Found:' in l:
                tmp = l.split(":")
                tmp2 = tmp[1].strip()
                keypoints = int(tmp2)
            if 'Keypoint algorithm time (s):' in l:
                tmp = l.split(":")
                tmp2 = tmp[1].strip()
                key_run_time = float(tmp2)
        data['particles'] = particles
        data['run_time'] = run_time
        data['key_run_time'] = key_run_time
        data['keypoints'] = keypoints
        return data

    
    def process(self):
        a = subprocess.call("int_process.py", shell=True)
        print a

    def process2(self):
        img = cv2.imread(r"../resources/matlab/capture.png")
        print img.dtype
        #maxIntensity = 255.0 # depends on dtype of image data
        
        #dst = img-mn
       
        #cv2.add(img, 100.0, dst=dst)

        scale_img = cv2.resize(img, (0,0), fx=2.0, fy=2.0)
        gray2 = cv2.cvtColor(scale_img,cv2.COLOR_BGR2GRAY)
        #gray = cv2.equalizeHist(gray2)
        
        mn = np.amin(gray2)
        dst2 = gray2-mn
        pk = np.amax(dst2)
        gray3 = 256*(dst2.astype(float)/pk.astype(float))
        gray = gray3.astype(np.uint8)
        print gray[100,100]
        
        sift = cv2.SIFT(edgeThreshold=2,contrastThreshold=0.02)
        kp = sift.detect(gray,None)

        img2=cv2.drawKeypoints(gray,kp, color = 256)

        cv2.imwrite(r"../resources/matlab/capture2.png",img2)

        kernel_size = 5
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S
        gray_lap = cv2.Laplacian(gray,ddepth,ksize = kernel_size,scale = scale,delta = delta)
        dst = cv2.convertScaleAbs(gray_lap)
        #dst2 = cv2.equalizeHist(dst)

        sift2 = cv2.ORB()
        kp = sift2.detect(dst)

        img2=cv2.drawKeypoints(dst,kp)

        #a = self.detect_peaks(gray)
        
        #imf = np.float32(gray)/255.0  # float conversion/scale
        #print imf[1, 1]
        #dst = cv2.dct(imf[1:513, 1:513])
        #img2 = np.uint8(dst)*255.0
        cv2.imwrite(r"../resources/matlab/capture3.png",img2)

        #img3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        #        cv2.THRESH_BINARY,11,2)

        #cv2.imwrite('capture3.png',img3)
        #plt.subplot(2,2,1),plt.imshow(img,'gray')
        #plt.subplot(2,2,2),plt.imshow(img2,'gray')
        #plt.subplot(2,2,3),plt.imshow(dst,'gray')
        #plt.imshow(dst2,'gray')
        #plt.show()


    def detect_peaks(self,image):
        """
        Takes an image and detect the peaks usingthe local maximum filter.
        Returns a boolean mask of the peaks (i.e. 1 when
        the pixel's value is the neighborhood maximum, 0 otherwise)
        """

        # define an 8-connected neighborhood
        neighborhood = generate_binary_structure(2,2)

        #apply the local maximum filter; all pixel of maximal value 
        #in their neighborhood are set to 1
        local_max = maximum_filter(image, footprint=neighborhood)==image
        #local_max is a mask that contains the peaks we are 
        #looking for, but also the background.
        #In order to isolate the peaks we must remove the background from the mask.

        #we create the mask of the background
        background = (image==0)

        #a little technicality: we must erode the background in order to 
        #successfully subtract it form local_max, otherwise a line will 
        #appear along the background border (artifact of the local maximum filter)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

        #we obtain the final mask, containing only peaks, 
        #by removing the background from the local_max mask
        detected_peaks = local_max - eroded_background

        return detected_peaks        
