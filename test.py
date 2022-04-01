from cv2 import waitKey
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
                        #    -DOC HINH ANH - TACH HINH ANH NHAN DIEN-

def Controller(imgSrc):
    img = cv2.imread(imgSrc)
    gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)                               #Tạo một bức ảnh xám từ bức ảnh gốc
    gray = cv2.medianBlur (gray, 5)                                             #Giảm nhiễu

    thresh = cv2.adaptiveThreshold (gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)                 #Lấy ảnh ngưỡng
    contours, h = cv2.findContours (thresh, 1,2)  

    largest_rectangle = [0,0,0]
    for cnt in contours:
        peri = 0.01*cv2.arcLength (cnt, True)                                      #khoảng cách tối đa từ đường bao đến đường bao gần đúng 10%
        approx = cv2.approxPolyDP (cnt,peri, True)                                 #Lấy gần đúng các đa giác, 
        if len(approx) == 4:   
            area = cv2.contourArea (cnt)                                           #Tính diện tích đa giác, lấy đa giác lớn nhất là biển số
            if area > largest_rectangle[0]:                                   
                largest_rectangle = [cv2.contourArea (cnt), cnt, approx]
    imgDrawCt = img.copy()
    cv2.drawContours(imgDrawCt, [largest_rectangle[1]],0, (0, 255, 0),8)          #Đánh dấu vùng contours vừa tìm được

    x,y,w,h = cv2.boundingRect(largest_rectangle[1])                              #Vẽ Hình chữ nhật gần đúng từ contours tìm được,
                                                                                  #w, h là chiều rộng và chiều cao của ma trận
    imageCrop = img [y:y+h, x:x+w]                                                #x, y của điểm trên bên trái của hình chữ nhật, 
    # cv2.imshow ('DANH DAU DOI TƯONG', img)
    # cv2.drawContours(img, [largest_rectangle[1]],0, (255, 255, 255),18)
    # cv2.imshow ('CAT KHUNG BIÊN SO', img)

    return img, thresh, imgDrawCt, imageCrop


#-----------------------Dự đoán biển số từ hình ảnh đã cắt bằng thư viện----------------------
def predict(img):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur (gray, (3, 3), 0)
    thresh = cv2.threshold (blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string (invert, lang='eng', config='--psm 6')
    return data


src = 'img1.jpg'
img, thresh, imgDrawCt, imageCrop = Controller(src)
cv2.imshow ('Default', img)
cv2.imshow ('Thresh', thresh)
cv2.imshow ('Img Draw Max Contours', imgDrawCt)
cv2.imshow ('imageCrop', imageCrop)
data = predict(imageCrop)
print("Thông tin biển số: ")
print(data)

waitKey()
