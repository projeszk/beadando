import cv2
import numpy as np

class Processor():
    def detectCannyEdges(self,img):
        return cv2.Canny(img,100,200)