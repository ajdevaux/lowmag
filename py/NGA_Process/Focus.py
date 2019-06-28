import cv2
import numpy as np
from matplotlib import pyplot as plt

class NGA_Process_Focus:
	cam = None
	stages = None

	def __init__(self, camera, stg):
		self.cam = camera
		self.stages = stg

	def score(self):
		debug = 0
		img = cv2.imread(r"..\\data\\capture_py.png", 2)
		blur = cv2.GaussianBlur(img, (11,11), 3)
		blur2 = cv2.GaussianBlur(img, (11,11), 1.5)
		blur = blur.astype('int16')
		blur2 = blur2.astype('int16')
		diff = blur - blur2
		diff = abs(diff)
		score = cv2.sumElems(diff)
		score = score[0]
		if debug:
			print score
			cv2.imshow("blur", blur)
			cv2.imshow("blur2", blur2)
			cv2.imshow("Diff", diff)
			cv2.waitKey()
			cv2.destroyAllWindows()
		return score

	#Thresholds the image and calculates percentage that is dark
	def percent_dark(self):
		img = cv2.imread("../data/capture_py.png",2)
		thresh = cv2.sumElems(img)[0] / img.size
		dark = 0;
		light = 0;
		#loop over pixels with stepsize 1/100 the size of the dimension
		for i in range(0,img.shape[0], img.shape[0]/100):
			for j in range(0, img.shape[1], img.shape[0]/100):
				if img[i][j] > thresh:
					light += 1
				else:
					dark += 1
		return dark/ float(dark + light)

	def brightness(self):
		img = cv2.imread("../data/capture_py.png")
		img = img.astype('int16')
		return cv2.sumElems(img)[0]

	def find_corner(self, quad):
		img = cv2.imread("../data/capture_py.png",2)
		thresh = cv2.sumElems(img)[0] / img.size
		print thresh
		i = 0
		j = 0
		if(quad == 0):
			while(img[0,i] < thresh):
				i += 1
			while(img[j,0] < thresh):
				j += 1
		elif(quad == 1):
			while(img[0,i] > thresh):
				i += 1
			while(img[j,img.shape[1]-1] < thresh):
				j += 1
		return i / float(img.shape[1]),j / float(img.shape[0])

	def quadrant(self):
		img = cv2.imread("../data/capture.png",2)
		thresh = cv2.sumElems(img)[0] / img.size
		if ((cv2.sumElems(img[0,:])[0] / img.shape[1]) < thresh):
			self.quad = 0
		else:
			self.quad = 2
		if ((cv2.sumElems(img[:,0])[0] / img.shape[0]) < thresh):
			self.quad += 0
		else:
			self.quad += 1
		return self.quad
