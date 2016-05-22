import cv2
import numpy as np

class Processor():
	"""
	Image processor.
	"""
	def detectCannyEdges(self,img):
		"""
		Execute canny edge detection.

		:param img: image to process
		:type img: numpy.array

		:return: processed image
		:rtype: numpy.array
		"""
		return cv2.Canny(img,100,200)
		

	def detectLaplacianEdges(self,img):
		"""
		Execute laplacian detection.

		:param img: image to process
		:type img: numpy.array

		:return: processed image
		:rtype: numpy.array
		"""
		return cv2.Laplacian(img,cv2.CV_64F)
		
	def haarCascadeDetection(self, img):
		"""
		Face Detection using Haar Cascades.

		:param img: image to process
		:type img: numpy.array

		:return: processed image
		:rtype: numpy.array
		"""	
		face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			eyes = eye_cascade.detectMultiScale(roi_gray)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
		
		return img
	
	def harrisCornerDetection(self, img):
		"""
		Harris corner detection.

		:param img: image to process
		:type img: numpy.array

		:return: processed image
		:rtype: numpy.array
		"""
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray = np.float32(gray)
		dst = cv2.cornerHarris(gray,2,3,0.04)
		dst = cv2.dilate(dst,None)
		img[dst>0.01*dst.max()]=[0,0,255]
		return img
	
	
	
	
	
	
	
		