from matplotlib import pyplot as plt
import numpy as np

class NGA_Process_Gauss:

    img = None
    KernelSize = 9
    Half_kernel = 0
    Sigma = 1
    Gauss = None
    GaussPatch = None
    GaussMean = 0
    GaussCorrCoef = 0
    Contrast = 0
    InnerRadius = 9
    OuterRadius = 12
    
    def __init__(self):
        self.GaussCorrCoef = 0
        self.Half_kernel = (self.KernelSize-1)/2
        self.Gauss = self.makeGaussian(self.KernelSize)
        self.GaussMean = np.mean(self.Gauss)
        self.GaussPatch = self.Gauss-self.GaussMean
        self.Contrast = 0
        self.GaussCorrCoef = 0
    def fit(self, kp, plta = False):
        tempXLoc = round(kp.pt[1])
        tempYLoc = round(kp.pt[0])
        XLocStart = tempXLoc-self.Half_kernel
        XLocEnd = tempXLoc+self.Half_kernel
        YLocStart = tempYLoc-self.Half_kernel
        YLocEnd = tempYLoc+self.Half_kernel

        #print "x: ",kp.pt[1], " y: ", kp.pt[0]

        #print "kp(x,y): " + str(tempXLoc) + "," + str(tempYLoc)
        #print "XStart: " + str(XLocStart) + "," + str(0)
        #print "YStart: " + str(YLocStart) + "," + str(0)
        #print "XEnd: " + str(XLocEnd) + "," + str(self.img.shape[1])
        #print "YEnd: " + str(YLocEnd) + "," + str(self.img.shape[0])
        if (XLocStart > 0) & (YLocStart > 0):
            if (XLocEnd < self.img.shape[0]) & (YLocEnd < self.img.shape[1]):
                self.GaussCorrCoef = 0.0
                TempImagePatch=self.img[XLocStart:XLocEnd,YLocStart:YLocEnd]
                
                TempImagePatch2=TempImagePatch-np.mean(TempImagePatch)
                
                #print self.GaussPatch.shape
                #print TempImagePatch2.shape
                sum1 = np.sum(self.GaussPatch**2)
                sum2 = np.sum(TempImagePatch2**2)
                sum3 = np.sqrt(sum1*sum2)
                np.seterr('print')
                self.GaussCorrCoef = np.sum(np.sum(self.GaussPatch*TempImagePatch2))/sum3
            else:
                self.GaussCorrCoef = 0.0
        else:
            self.GaussCorrCoef = 0.0

        if (plta == True):
                plt.imshow(self.GaussPatch*TempImagePatch2)
                plt.title(str(self.GaussCorrCoef))
                plt.show()
                    
        return self.GaussCorrCoef
            
    def contrast(self, kp):
        xi = round(kp.pt[1])
        yi = round(kp.pt[0])
        val = 0
        vals = []
        pk = self.img[xi,yi]
        for i1 in range(-1*self.OuterRadius, self.OuterRadius, 1):
            if ((yi+i1)<1):
                continue
            elif ((yi+i1) >= self.img.shape[1]):
                continue
            else:
                for i2 in range(-1*self.InnerRadius, self.InnerRadius, 1):
                    if ((xi+i2)<1):
                        continue
                    elif ((xi+i2)>= self.img.shape[0]):
                        continue
                    else:
                        r_temp = i1**2 + i2**2
                        if ((r_temp < (self.OuterRadius**2)) & (r_temp > (self.InnerRadius**2))):
                            val = val + 1
                            vals = np.append(vals,self.img[xi+i2,yi+i1])

        contrast_val = pk - np.median(vals)
        #print "Peak: " + str(pk)
        #print "Constrast: " + str(contrast_val)
        return contrast_val

        
    def makeGaussian(self, size, fwhm = 3, center=None):
        """ Make a square gaussian kernel.

        size is the length of a side of the square
        fwhm is full-width-half-maximum, which
        can be thought of as an effective radius.
        """

        x = np.arange(1, size, 1, float)
        y = x[:,np.newaxis]

        if center is None:
            x0 = y0 = size // 2
        else:
            x0 = center[0]
            y0 = center[1]

        
        return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)


if __name__ == '__main__':
    NGA = NGA_Process_Gauss()
    
