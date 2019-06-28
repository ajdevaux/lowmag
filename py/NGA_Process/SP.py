import cv2
import sys
from scipy import fftpack, signal
#from scipy import *
from PIL import Image, ImageTk
import numpy as np
from matplotlib import pyplot as plt
from pylab import *
from array import *
#from scipy import optimize

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion
from scipy.signal import correlate2d

from NGA_Process.Gauss import NGA_Process_Gauss
from NGA_Image.Image import NGA_Image

import time

class NGA_Process_SP:

    fn = ""
    out_d = None
    
    def __init__(self, imgfn):
        self.fn = imgfn
        self.out_d = dict()

    def process(self):
        start_time = time.time()
        #if (len(sys.argv) == 2):
        #       fn = r"../resources/matlab/" + str(sys.argv[1])
        #else:
        #       fn = r"../resources/matlab/capturea.png"

        imscale = 2
        
        fn2 = r"../resources/matlab/capture2.png"
        fn3 = r"../resources/matlab/capture3.png"
        fn4 = r"../resources/matlab/process.png"

        fn_temp = r"../resources/matlab/out_temp.png"

        # convert RGB png to GRAY PNG
        # still keep 16-bit resolution
        #img_temp_1 = cv2.imread(fn,-1)
        #img_temp_gray = cv2.cvtColor(img_temp_1,cv2.COLOR_BGR2GRAY)
        #cv2.imwrite(fn_temp,plt.contour(img_temp_gray))

        #im = Image.open(fn).convert('L')
        #im2 = contour(im, origin='image')
        #im2.save(fn_temp)

        img = cv2.imread(self.fn) #reads png as 8-bit
        #img = imgt[900:1200,1400:1500]
        #img = imgt
        #print img.dtype
        
        # if 8-bit files, which are the ones compatible with SURF
        maxIntensity = 255.0 # depends on dtype of image data
        percentContrast = 100.0/maxIntensity

        gauss = NGA_Process_Gauss()

        gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        scale_img = cv2.resize(gray2, (0,0), fx=imscale, fy=imscale)

        
        surf = cv2.SURF(hessianThreshold=5) #SIFT(edgeThreshold=2,contrastThreshold=0.005)
        kp = surf.detect(scale_img,None)

        self.out_d['kp'] = len(kp)
        self.out_d['kp_t'] = time.time() - start_time
        print "Keypoints Found: {0}".format(len(kp))
        print "Keypoint algorithm time (s): {0:.2f}".format(time.time() - start_time)
        #gray_rgb = cv2.cvtColor(scale_img,cv2.COLOR_BGR2GRAY)
        cnt = 0
        cnt2 = 0
        sze = 8
        tt = None
        part_cnt = 0
        hist_bins = np.array([])
        hist_bins1 = np.array([])
        hist_bins2 = np.array([])
        cor_bin = np.array([])
        kp1 = np.array([])
        kp2 = np.array([])
        kp3 = np.array([])
        kp4 = np.array([])
        gauss.img = scale_img
        for xi in range(len(kp)):
            x = kp[xi].pt[1]/imscale
            y = kp[xi].pt[0]/imscale
            if cnt == 8e12:
                gauss_cor = gauss.fit(kp[xi], True)
            else:
                gauss_cor = gauss.fit(kp[xi], False)
            cor_bin = np.append(cor_bin,gauss_cor)
            #print gauss_cor
            t_kp = cv2.KeyPoint(y,x,kp[xi].size)
            kp1 = np.append(kp1,t_kp)
            if gauss_cor > 0.2:
                contrast = gauss.contrast(kp[xi])*percentContrast
                #print contrast
                hist_bins = np.append(hist_bins,contrast)
                if ((contrast > 3) & (contrast < 12)):
                    part_cnt = part_cnt + 1
                    kp2 = np.append(kp2,t_kp)
                    hist_bins1 = np.append(hist_bins1,contrast)
                elif (contrast <= 2):
                    kp3 = np.append(kp3,t_kp)
                    hist_bins2 = np.append(hist_bins2,contrast)
                else:
                    kp4 = np.append(kp4,t_kp)
                    hist_bins2 = np.append(hist_bins2,contrast)

        self.out_d['particles'] = part_cnt
        self.out_d['particles_t'] = time.time() - start_time
        print "Particles Found: {0}".format(part_cnt)
        print "Particle Finding time (s): {0:.2f}".format(time.time() - start_time)
        gauss.img = gray2

        dst3 = cv2.equalizeHist(gray2)

        # found virions
        img2b=cv2.drawKeypoints(dst3,kp2, color = (0,128,0))
        # under particles
        img2c=cv2.drawKeypoints(img2b,kp3, color = (0,0,128))
        # over particles
        img2=cv2.drawKeypoints(img2c,kp4, color = (128,0,0)) 
        #img2b = cv2.resize(img2, (0,0), fx=(1.0/imscale), fy=(1.0/imscale))
        cv2.imwrite(fn2,img2)
        self.out_d['delta_t'] = time.time() - start_time
        print "entire run time (s): {0:.2f}".format(time.time() - start_time)
        
        img3 = cv2.drawKeypoints(gray2,kp1, color = (128,0,0)) 
        cv2.imwrite(fn3,img3)

        fig2 = plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
        ax1 = plt.axes([0.05, 0.05, 0.55, 0.9])
        plt.imshow(img2)
        plt.title("Particles Found: {0}".format(part_cnt))
  
        # CONTRAST HISTOGRAMS
        ax2 = plt.axes([0.7, 0.05, 0.25, 0.25])
        
        plt.hist(hist_bins1,10,alpha=0.75,color='green')
        plt.hold(True)
        plt.hist(hist_bins2,50,alpha=0.75,color='red')
        ax2.set_xlim([-10,25])
        mu = np.mean(hist_bins1)
        sigma = np.std(hist_bins1)
        ttl = r'$\mu: {mu:0.2f},   \sigma: {sigma:0.2f}$'.format(mu=mu, sigma=sigma)
        #ttl = r'$\mu=' + str(mu) + r', \sigma=' + str(sigma) + '$'
        plt.title(ttl)
        #plt.subplot(1,2,2)

        ## CORR HISTOGRAM
        
        cor_bin_f = cor_bin[np.logical_not(np.isnan(cor_bin))]
        ax3 = plt.axes([0.7, 0.4, 0.25, 0.25])
        #plt.hist(cor_bin,10,alpha=0.75,color='blue')
        hist, bins = np.histogram(cor_bin_f.ravel(), bins=256, density=True)
        bincenters = 0.5*(bins[1:]+bins[:-1])
        plt.plot(bincenters,hist)
        mu = np.mean(cor_bin_f)
        sigma = np.std(cor_bin_f)
        ttl = r'$\mu: {mu:0.2f},   \sigma: {sigma:0.2f}$'.format(mu=mu, sigma=sigma)
        #ttl = r'$\mu=' + str(mu) + r', \sigma=' + str(sigma) + '$'
        plt.title(ttl)
        #plt.subplot(1,2,2)

        
        #plt.show()
        plt.savefig(fn4)
        
        return self.out_d

