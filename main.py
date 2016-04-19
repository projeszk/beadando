from imgprocessing import processor
import cv2
import numpy as np

image = cv2.imread("./testimages/test2.png")
proc = processor.Processor()
edges = proc.detectCannyEdges(image)
cv2.imshow("picture",edges)
cv2.waitKey(2000)