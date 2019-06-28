import cv2
from matplotlib import pyplot as plt
import numpy as np

from NGA_Utils.Text_Config import NGA_Text_Config


class NGA_Image:

    fn = r"..\data\capture_py.png"
    fn_info = r"..\data\capture_py.txt"
    info = None
    img = None
    
    def __init__(self):
        self.load()
        #if key == 27:
        #    cv2.destroyWindow(winName)

    def load(self):
        self.img = cv2.imread(self.fn)
        self.collect_info()
        key = cv2.waitKey(1)
        
    def collect_info(self):
        self.info = NGA_Text_Config(self.fn_info)
        #self.info.recall_config()

    def imshow(self):
        if self.img != None:
            cv2.imshow(self.fn, self.img)
            cv2.moveWindow(self.fn, 750, 100)
            
    def imclose(self):
        if self.img != None:
            cv2.destroyWindow(self.fn)

    def imhist(self):
        if self.img != None:
            
            bin_n = 256;
            hist, bins = np.histogram(self.img.ravel(), bins=bin_n, density=True)
            elem = np.argmax(hist)
            print "Peak Value: " + str(bins[elem]/(bin_n-1))

            plt.hist(self.img.ravel()/256.0,256,[0,1])
            plt.show()
            #width = 1.0
            #center = (bins[:-1] + bins[1:]) / 2
            #plt.bar(center, hist)
            #plt.show()
