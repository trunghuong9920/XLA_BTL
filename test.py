from operator import le
from cv2 import waitKey
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract


def displayImg(image, nameWindow="Image View"):
    cv2.imshow(nameWindow, image)
    cv2.waitKey(0)

                        #    -DOC HINH ANH - TACH HINH ANH NHAN DIEN-
img = cv2.imread('img_moto/img2.jpg')
cv2.imshow ('HINH ANH GỌC', img)
gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold (gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
contours, h = cv2.findContours (thresh, 1,2)
largest_rectangle = [0,0]
for cnt in contours:
    approx = cv2.approxPolyDP (cnt, 0.01*cv2.arcLength (cnt, True), True)
    if len(approx) == 4:   
        area = cv2.contourArea (cnt)
        if area > largest_rectangle[0]:
            largest_rectangle = [cv2.contourArea (cnt), cnt, approx]
x,y,w,h = cv2.boundingRect(largest_rectangle[1])
image=img[y:y+h, x:x+w]
cv2.drawContours(img, [largest_rectangle[1]],0, (0, 255, 0),8)
cropped = img [y:y+h, x:x+w]
# cv2.imshow ('DANH DAU DOI TƯONG', img)
cv2.drawContours(img, [largest_rectangle[1]],0, (255, 255, 255),18)
# cv2.imshow ('CAT KHUNG BIÊN SO', img)




waitKey()