import cv2
import numpy as np
from scipy import ndimage
import math
import sys
from matplotlib import pyplot as plt
from scipy.ndimage import label

import NGA_Process.IRIS as NGA_Process_IRIS

class NGA_Interface_IRIS:

    img = None
    sr_mask = None
    
    def __init__(self):
        self.img = None
        self.sr_mask = None

    def remove_sr(self, img):
        img_t = cv2.imread(img)
        img1 = cv2.cvtColor(img_t,cv2.COLOR_BGR2GRAY)
        bin_n = 64;
        hist, bins = np.histogram(img1.ravel(), bins=bin_n, density=True)
        elem = np.argmax(hist)
        elem2 = np.argsort(hist)
        #print elem2
        print "Histogram Peak: ", bins[elem]
        std = np.sqrt(np.std(bins))
        print "STD: ", std
        max1 = bins[elem2[-1]]
        max2 = 0
        for i in reversed(elem2):
            if (max2 == 0) & (abs(bins[i]-max1) > std):
                print bins[i]
                max2 = bins[i]

        thresh_val = (max1+max2)/2
        print "Threshold = ", thresh_val

        img_er = img1.copy()
        x, y = (img1 > thresh_val).nonzero()
        img_t[x, y] = (0, 0, 255)
        img_er[x, y] = 0 
        #ret,thresh = cv2.threshold(img1,thresh_val,255,cv2.THRESH_BINARY)
        #cv2.imshow('detected sr',img_er)
        #cv2.waitKey()
        element = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
        eroded = cv2.erode(img_er,element)
        ret, mask = cv2.threshold(eroded, 0, 255, cv2.THRESH_BINARY)
        self.sr_mask = mask
        
        #cv2.imshow('detected sr',eroded)
        #cv2.waitKey()
        
    def spot(self, img_fn):
        img_t = cv2.imread(img_fn)
        img = img_t #img_t[30:550,50:500]
        #bin_n = 256;
        #hist, bins = np.histogram(img.ravel(), bins=bin_n, density=True)
        #elem = np.argmax(hist)
        #print "Histogram Peak: ", elem
        #(thresh, im_bw) = cv2.threshold(img, elem, 256, cv2.THRESH_BINARY)
            
        self.circles5(img)
        #cv2.imshow('Look for Spots',im_bw)
        cv2.waitKey()
        #sys.exit()

    def circles5(self, img):

        img1t2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img1t = cv2.bitwise_and(img1t2,img1t2, mask=self.sr_mask)

        img1 = cv2.medianBlur(img1t,23)
        img1t3 = cv2.medianBlur(img1t2,23)
        img3 = cv2.equalizeHist(img1t)
        
        bin_n = 64;
        vals = img1.flatten()
        nz = np.nonzero(vals)
        hist, bins = np.histogram(vals[nz], bins=bin_n, density=True)
        elem = np.argmax(hist)
        elem2 = np.argsort(hist)
        #print elem2
        print "Histogram Peak: ", bins[elem]
        std = np.sqrt(np.std(bins))
        print "STD: ", std
        max1 = bins[elem2[-1]]
        max2 = 0
        for i in reversed(elem2):
            if (max2 == 0) & (abs(bins[i]-max1) > std):
                print bins[i]
                max2 = bins[i]

        thresh_val = (max1+max2)/2
        print "Threshold = ", thresh_val

        
        
        
        ret,thresh = cv2.threshold(img1t3,thresh_val,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            M = cv2.contourArea(cnt)
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            if radius > 15:
                print "Found Circle, r = ", radius
                cv2.circle(img3,center,radius,(0,255,0),2)
                #cv2.drawContours(img3,cnt,0,(0,255,0))

        img3b = cv2.bitwise_and(img3,img3, mask=self.sr_mask)
        img4 = cv2.resize(img3b, (0,0), fx=2.0, fy=2.0)
        cv2.imshow('detected circles',img4)
        cv2.imwrite(r"../resources/matlab/dd.png", img1)
    
    def circles4(self, img):
        

        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img2 = cv2.medianBlur(img1,5)
        
        img3 = cv2.equalizeHist(img2)
        
        circles = cv2.HoughCircles(img3,cv2.cv.CV_HOUGH_GRADIENT,2,100,
                                param1=10,param2=20,minRadius=5,maxRadius=35)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img3,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(img3,(i[0],i[1]),2,(0,0,255),3)

        
        cv2.imshow('detected circles',img3)

    def circles3(self, img):
        cimg = cv2.medianBlur(img,5)
        img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.equalizeHist(img2)
        circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,2,20,
                                param1=50,param2=30,minRadius=0,maxRadius=40)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        cv2.imshow('detected circles',cimg)

    def circles2(self, im):
        obj_center =  None
        #hgh = cv.HoughCircles(img, storage, cv.CV_HOUGH_GRADIENT, 1, 16.0, 180, 220)
        circles, new_center = self.find_circles(im)
        if obj_center is None:
            obj_center = [(str(i + 1), c) for i, c in enumerate(new_center)]
        else:
            self.track_center(obj_center, new_center)

        for i in xrange(len(circles)):
            cv2.drawContours(im, circles, i, (0, 255, 0))
            cstr, ccenter = obj_center[i]
            cv2.putText(im, cstr, ccenter, cv2.FONT_HERSHEY_COMPLEX, 0.5,
                    (255, 255, 255), 1, cv2.CV_AA)

        cv2.imshow("result", im)

    def segment_on_dt(self, img):
        border = img - cv2.erode(img, None)

        dt = cv2.distanceTransform(255 - img, 2, 3)
        dt = ((dt - dt.min()) / (dt.max() - dt.min()) * 255).astype(np.uint8)
        _, dt = cv2.threshold(dt, 100, 255, cv2.THRESH_BINARY)

        lbl, ncc = label(dt)
        lbl[border == 255] = ncc + 1

        lbl = lbl.astype(np.int32)
        cv2.watershed(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB), lbl)
        lbl[lbl < 1] = 0
        lbl[lbl > ncc] = 0

        lbl = lbl.astype(np.uint8)
        lbl = cv2.erode(lbl, None)
        lbl[lbl != 0] = 255
        return lbl


    def find_circles(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame_gray = cv2.GaussianBlur(frame_gray, (5, 5), 2)

        edges = frame_gray - cv2.erode(frame_gray, None)
        _, bin_edge = cv2.threshold(edges, 0, 255, cv2.THRESH_OTSU)
        cv2.imshow("bin", bin_edge)
        height, width = bin_edge.shape
        mask = np.zeros((height+2, width+2), dtype=np.uint8)
        cv2.floodFill(bin_edge, mask, (0, 0), 255)

        components = self.segment_on_dt(bin_edge)

        circles, obj_center = [], []
        contours, _ = cv2.findContours(components,
                cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            c = c.astype(np.int64) # XXX OpenCV bug.
            area = cv2.contourArea(c)
            if 10 < area < 30000:
                arclen = cv2.arcLength(c, True)
                circularity = ((4*math.pi) * area) / (arclen * arclen)
                if circularity > 0.5: # XXX Yes, pretty low threshold.
                    circles.append(c)
                    box = cv2.boundingRect(c)
                    obj_center.append((box[0] + (box[2] / 2), box[1] + (box[3] / 2)))

        return circles, obj_center

    def track_center(self, objcenter, newdata):
        for i in xrange(len(objcenter)):
            ostr, oc = objcenter[i]
            best = min((abs(c[0]-oc[0])**2+abs(c[1]-oc[1])**2, j)
                    for j, c in enumerate(newdata))
            j = best[1]
            if i == j:
                objcenter[i] = (ostr, new_center[j])
            else:
                print "Swapping %s <-> %s" % ((i, objcenter[i]), (j, objcenter[j]))
                objcenter[i], objcenter[j] = objcenter[j], objcenter[i]

    def circles(self, im):
        height, width, depth = im.shape
        print height, width, depth
        thresh = 132
        imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(imgray,(3,3),0)
        edges = cv2.Canny(blur,thresh,thresh*2)
        contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        cv2.drawContours(im,contours,-1,(0,255,0),-1)

        #centroid_x = M10/M00 and centroid_y = M01/M00
        M = cv2.moments(cnt)
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
        print x,y
        print width/2.0,height/2.0
        print width/2-x,height/2-y


        cv2.circle(im,(x,y),1,(0,0,255),2)
        cv2.putText(im,"center of Sun contour", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))
        cv2.circle(im,(width/2,height/2),1,(255,0,0),2)
        cv2.putText(im,"center of image", (width/2,height/2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0))
        cv2.imshow('contour',im)
        #cv2.waitKey(0)
    def load(self, img_fn):

        extra_pixels = 20
        self.img = cv2.imread(img_fn)
        timg = self.img.copy()
        cimg = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        #cimg = ndimage.rotate(cimgtt, 10)

        if (0):
            (thresh, im_bw) = cv2.threshold(cimg, 128, 16, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            #thresh = 127
            print "Thresh:", thresh
            thr, im_bw2 = cv2.threshold(cimg, thresh, 255, cv2.THRESH_BINARY)
            cv2.imwrite(r"../resources/matlab/bw_image.png", im_bw2)

            cny = cv2.Canny(cimg,100,200)
            cv2.imwrite(r"../resources/matlab/bw_image2.png", cny)
            contours,hierarchy = cv2.findContours(cny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cntarea = cv2.contourArea(cnt)
                
                if (cntarea > 200000) & (cntarea < 600000):
                    print "Area:", cntarea
                    #M = cv2.moments(cnt)
                    print cnt
                    x,y,w,h = cv2.boundingRect(cnt)
                    color = np.random.randint(0,255,(3)).tolist()  # Select a random color
                    cv2.drawContours(timg,[cnt],0,color,20)
                    ntimg2 = cny[y-extra_pixels:y+h+extra_pixels,
                                 x-extra_pixels:x+w+extra_pixels]
                    cv2.imshow('output2',ntimg2)
            cv2.imwrite(r"../resources/matlab/contours2.png", ntimg2)


        if (1):

            #im = cv2.imread(img_fn)
            
            #imgray = cv2.cvtColor(cimg,cv2.COLOR_BGR2GRAY)
            (thresh, im_bw) = cv2.threshold(cimg, 128, 16, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
           
            ret,thresh_img = cv2.threshold(cimg,thresh,255, cv2.THRESH_BINARY)
            contours,hierarchy = cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cntarea = cv2.contourArea(cnt)
                
                if (cntarea > 200000) & (cntarea < 600000):
                    #print "Area:", cntarea
                    #M = cv2.moments(cnt)
                    
                    x,y,w,h = cv2.boundingRect(cnt)
                    color = np.random.randint(0,255,(3)).tolist()  # Select a random color
                    cv2.drawContours(timg,[cnt],0,color,2)
                    ntimg = cimg[y-extra_pixels:y+h+extra_pixels,
                                 x-extra_pixels:x+w+extra_pixels]
                    ntimg_active = cimg[y+extra_pixels:y+h-extra_pixels,
                                 x+extra_pixels:x+w-extra_pixels]
                    (thresh, im_bw) = cv2.threshold(ntimg, 128, 16, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
           
                    thr, im_bw2 = cv2.threshold(ntimg, thresh, 255, cv2.THRESH_BINARY)
                    #cv2.imshow('output',im_bw2)
                    angle_median = self.find_corners(cimg,cnt, x, y)
                    cimgr = ndimage.rotate(cimg, angle_median)
                    cv2.imwrite(r"../resources/matlab/contours.png", cimgr)
                    cv2.imwrite(r"../resources/matlab/contoursb.png", cimg)
                    cv2.imwrite(r"../resources/matlab/contours_spot.png", ntimg)
                    cv2.imwrite(r"../resources/matlab/contours_spot2.png", ntimg_active)

            im = cv2.imread(r"../resources/matlab/contours.png")
            
            imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            ret,im_bw = cv2.threshold(imgray,thresh,255, cv2.THRESH_BINARY)
            cv2.imwrite(r"../resources/matlab/contoursc.png", im_bw)
            contours,hierarchy = cv2.findContours(im_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cntarea = cv2.contourArea(cnt)
                if (cntarea > 200000) & (cntarea < 600000):
                    #print "Area:", cntarea
                    #M = cv2.moments(cnt)
                    
                    x,y,w,h = cv2.boundingRect(cnt)
                    color = np.random.randint(0,255,(3)).tolist()  # Select a random color
                    #cv2.drawContours(imgray,[cnt],0,color,2)
                    ntimg = imgray[y-extra_pixels:y+h+extra_pixels,
                                 x-extra_pixels:x+w+extra_pixels]
                    cv2.imwrite(r"../resources/matlab/contoursd.png", ntimg)
                    cv2.imshow('Detected Active Area',ntimg)
                    #cv2.imwrite(r"../resources/matlab/contourse.png", imgray)

        if (0):
            cimgr = ndimage.rotate(cimg, -1)

            # corner detection
            gray = np.float32(cimg)
            dst = cv2.cornerHarris(gray,2,3,0.04)
            dst = cv2.dilate(dst,None)
            cimg[dst>0.01*dst.max()]=[255]
            
            # circle detection
            gray3 = cv2.medianBlur(cimgr,5)
            circles = cv2.HoughCircles(gray3,cv2.cv.CV_HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=40)

            
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

            #cv2.imshow('detected circles',cimg)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    def find_corners(self,img,cnt,startx,starty):
        ne = [1e6,1e6]
        nw = [0,0]
        se = [0,0]
        sw = [0,0]
        #print img.shape

        # false values to replace
        max_x = 0
        max_y = 0
        min_x = 1e30
        min_y = 1e30

        min_sw = 1e30
        min_se = 1e30
        min_ne = 1e30
        min_nw = 1e30
        
        # find max, min of x and y
        for twp in cnt:
            temp = twp[0]
            x = temp[0]#-startx
            y = temp[1]#-starty
            if (x < min_x):
                min_x = x
            if (y < min_y):
                min_y = y
            if (x > max_x):
                max_x = x
            if (y > max_y):
                max_y = y

        #print "minx: ", min_x, " miny: ", min_y, " maxx: ", max_x, " maxy:", max_y
            
        for twp in cnt:
            temp = twp[0]
            x = temp[0]#-startx
            y = temp[1]#-starty
            #if (x - ne[0]) +(y - ne[1]) < 0:
            #    ne = [y,x]
            #if (x - nw[0]) +(y - nw[1]) > 0:
            #    nw = [y,x]
            if (abs(x - min_x)+abs(y - min_y)) < min_nw:
                min_nw = abs(x - min_x)+abs(y - min_y)
                #print min_ne
                nw = [y,x]
            if (abs(x - max_x)+abs(y - max_y)) < min_se:
                min_se = abs(x - max_x)+abs(y - max_y)
                #print min_nw
                se = [y,x]
            if (abs(x - max_x)+abs(y - min_y)) < min_ne:
                min_ne = abs(x - max_x)+abs(y - min_y)
                #print min_sw
                ne = [y,x]
            if (abs(x - min_x)+abs(y - max_y)) < min_sw:
                min_sw = abs(x - min_x)+abs(y - max_y)
                #print min_se
                sw = [y,x]

        ne1 = ne
        #print "ne: ", ne
        #print "nw: ", nw
        #print "se: ", se
        #print "sw: ", sw

        opp = nw[0]-ne[0]
        adj = ne[1]-nw[1]
        #print opp,",",adj
        ang1 = math.atan2(opp,adj)*(180/np.pi)
        #print ang1

        opp = se[0]-ne[0]
        adj = se[1]-ne[1]
        #print opp,",",adj
        ang2 = math.atan2(adj,opp)*(180/np.pi)
        #print ang2

        opp = sw[0]-se[0]
        adj = se[1]-sw[1]
        #print opp,",",adj
        ang3 = math.atan2(opp,adj)*(180/np.pi)
        #print ang3

        opp = sw[0]-nw[0]
        adj = sw[1]-nw[1]
        #print opp,",",adj
        ang4 = math.atan2(adj,opp)*(180/np.pi)
        #print ang4

        angle_median = -1*np.median([ang1,ang2,ang3,ang4])
        print "Median angle (deg): {0:.2f}".format(angle_median)
        
        if (0):
            newcolor = 255
            for twp in cnt:
                break
                temp = twp[0]
                ne = [temp[1], temp[0]]
                img[ne[0],ne[1]-1] = newcolor
                img[ne[0],ne[1]] = newcolor
                img[ne[0],ne[1]+1] = newcolor
                img[ne[0]-1,ne[1]-1] = newcolor
                img[ne[0]-1,ne[1]] = newcolor
                img[ne[0]-1,ne[1]+1] = newcolor
                img[ne[0]+1,ne[1]-1] = newcolor
                img[ne[0]+1,ne[1]] = newcolor
                img[ne[0]+1,ne[1]+1] = newcolor

            ne = ne1
            newcolor = 90 #white
            img[ne[0],ne[1]-1] = newcolor
            img[ne[0],ne[1]] = newcolor
            img[ne[0],ne[1]+1] = newcolor
            img[ne[0]-1,ne[1]-1] = newcolor
            img[ne[0]-1,ne[1]] = newcolor
            img[ne[0]-1,ne[1]+1] = newcolor
            img[ne[0]+1,ne[1]-1] = newcolor
            img[ne[0]+1,ne[1]] = newcolor
            img[ne[0]+1,ne[1]+1] = newcolor
            cv2.imshow('output',img)

            newcolor = 160
            img[nw[0],nw[1]-1] = newcolor
            img[nw[0],nw[1]] = newcolor
            img[nw[0],nw[1]+1] = newcolor
            img[nw[0]-1,nw[1]-1] = newcolor
            img[nw[0]-1,nw[1]] = newcolor
            img[nw[0]-1,nw[1]+1] = newcolor
            img[nw[0]+1,nw[1]-1] = newcolor
            img[nw[0]+1,nw[1]] = newcolor
            img[nw[0]+1,nw[1]+1] = newcolor

            newcolor = 255 #white
            img[sw[0],sw[1]-1] = newcolor
            img[sw[0],sw[1]] = newcolor
            img[sw[0],sw[1]+1] = newcolor
            img[sw[0]-1,sw[1]-1] = newcolor
            img[sw[0]-1,sw[1]] = newcolor
            img[sw[0]-1,sw[1]+1] = newcolor
            img[sw[0]+1,sw[1]-1] = newcolor
            img[sw[0]+1,sw[1]] = newcolor
            img[sw[0]+1,sw[1]+1] = newcolor

            newcolor = 0 #black
            img[se[0],se[1]-1] = newcolor
            img[se[0],se[1]] = newcolor
            img[se[0],se[1]+1] = newcolor
            img[se[0]-1,se[1]-1] = newcolor
            img[se[0]-1,se[1]] = newcolor
            img[se[0]-1,se[1]+1] = newcolor
            img[se[0]+1,se[1]-1] = newcolor
            img[se[0]+1,se[1]] = newcolor
            img[se[0]+1,se[1]+1] = newcolor

        return angle_median
        #cimgr = ndimage.rotate(img, angle_median)
        #cv2.imshow('output',img)
