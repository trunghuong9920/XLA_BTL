from operator import le
from cv2 import waitKey
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract


# def displayImg(image, nameWindow="Image View"):
#     cv2.imshow(nameWindow, image)
#     cv2.waitKey(0)

#                         #    -DOC HINH ANH - TACH HINH ANH NHAN DIEN-
# img = cv2.imread('img_moto/img2.jpg')
# cv2.imshow ('HINH ANH GỌC', img)
# gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
# thresh = cv2.adaptiveThreshold (gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
# contours, h = cv2.findContours (thresh, 1,2)
# largest_rectangle = [0,0]
# for cnt in contours:
#     approx = cv2.approxPolyDP (cnt, 0.01*cv2.arcLength (cnt, True), True)
#     if len(approx) == 4:   
#         area = cv2.contourArea (cnt)
#         if area > largest_rectangle[0]:
#             largest_rectangle = [cv2.contourArea (cnt), cnt, approx]
# x,y,w,h = cv2.boundingRect(largest_rectangle[1])
# image=img[y:y+h, x:x+w]
# cv2.drawContours(img, [largest_rectangle[1]],0, (0, 255, 0),8)
# cropped = img [y:y+h, x:x+w]
# # cv2.imshow ('DANH DAU DOI TƯONG', img)
# cv2.drawContours(img, [largest_rectangle[1]],0, (255, 255, 255),18)
# # cv2.imshow ('CAT KHUNG BIÊN SO', img)

# WIDTH = 640
# HEIGHT = 480
# image = cv2.resize(image, (WIDTH, HEIGHT))
# grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blurImg = cv2.GaussianBlur(grayImg, (9,9), 0, 0)
# thImg = cv2.threshold(blurImg, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]

# cnt, _ = cv2.findContours(thImg,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# lines = []
# for c in cnt:
#     if cv2.contourArea(c) < 15:
#         continue
#     else:
#         x,y,w,h = cv2.boundingRect(c)
#         lines.extend([[x,y,w,h]])

# kernel =np.array([[0,1,1,0,0],
#             [1,1,1,1,1],
#             [1,1,1,1,1],
#             [1,1,1,1,1],
#             [0,1,1,0,0]],np.uint8)

# arr = []
# for x,y,w,h in reversed(lines):
#     # Find contours cho từng chữ trong ảnh
#     line = image[y:y+h, x:x+w]

#     line = cv2.morphologyEx(line, cv2.MORPH_CLOSE,kernel)
#     # cnt, _ = cv2.findContours(line,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#     # for c in cnt:
#     #     if cv2.contourArea(c) < 15:
#     #         continue
#     #     arr.append(c)
#     #     x1,y1,w1,h1 = cv2.boundingRect(c)

#     #     # Vẽ bbox cho từng chữ trong ảnh
#     #     cv2.rectangle(image[y:y+h, x:x+w],(x1,y1), (x1+w1-1, y1+h1-1),(0,0,255),1)
#     displayImg(line,"Line View ")

# DOC HINH ANH CHUYEN THANH FILE TEXT-

# img = cv2.imread('img_moto/test3.jpg')

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur (gray, (3, 3), 0)
# thresh = cv2.threshold (blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# cv2.imshow ('Defaul', thresh)

# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
# invert = 255 - opening
# data = pytesseract.image_to_string (invert, lang='eng', config='--psm 6')

# print ("THONG TIN NHAN DIEN: ")
# print (data)

img = cv2.imread('img_moto/test3.jpg')
cv2.imshow ('HINH ANH GỌC', img)
custom_config = r'--oem 3 --psm 6'
# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
preimage = get_grayscale(img)
text = pytesseract.image_to_string(preimage, config=custom_config)
print(text)

waitKey()