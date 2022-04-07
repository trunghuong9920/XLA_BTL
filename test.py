import cv2 as cv
import cv2
from cv2 import waitKey
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('img_moto/img2.jpg',0)


img = cv2.medianBlur(img,5)
ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
print(ret)
cv.imshow("rda", th1)

waitKey()