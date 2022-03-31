from cv2 import waitKey
import numpy as np
import cv2
import sys
import pytesseract
import matplotlib.pyplot as plt
from PIL import Image
from tkinter import filedialog as fd
from tkinter import *
from PIL import Image, ImageTk

                        #  -DOC HINH ANH - TACH HINH ANH NHAN DIEN-
def handleImg(imgSrc):
    img = cv2.imread(imgSrc)
    cv2.imshow ('HINH ANH GỌC', img)
    gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold (gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)
    contours, h = cv2.findContours(thresh, 1,2)
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
    cv2.imshow ('DANH DAU DOI TƯONG', img)
    cv2.drawContours(img, [largest_rectangle[1]],0, (255, 255, 255),18)
    cv2.imshow ('CAT KHUNG BIÊN SO', img)
    return image

# DOC HINH ANH CHUYEN THANH FILE TEXT-
def readImg(image):
    pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    gray = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur (gray, (3, 3), 0)
    thresh = cv2.threshold (blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) [1]
    cv2.imshow('CROP', thresh)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    invert = 255 - opening
    data = pytesseract.image_to_string (invert, lang='eng', config='--psm 6')
    return data

# waitKey()

def getImage():
    filetypes = (
        ('text files', '*.jpg'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    image = handleImg(filename)
    data = readImg(image)
    label_show.set(data)


def close():
    sys.exit()

root =Tk()
# root.geometry("600x350")
root.option_add("*Font","TimeNewRoman 14")
label_show=StringVar()

Label (root, text="Nhận diện biển số xe máy với opencv và pytesseract").grid(row=0,columnspan=2)
Button (root, text="Chọn ảnh",bg= 'cyan', command=getImage).grid(row=8,columnspan=2,padx=10,pady=10,sticky = E)
Button (root, text="Thoát",bg= 'cyan', command=close).grid(row=9,columnspan=2,padx=10,pady=10,sticky = E)

Label (root, text="Kết quả:").grid(row=1,column=0,padx=10,pady=10,sticky = W)
Label(root,textvariable=label_show).grid(row=2,column=0,padx=10,pady=10,sticky = W)

# basewidth = 300
# imgDefaul= Image.open("xemay2.jpg")
# wpercent = (basewidth / float(imgDefaul.size[0]))
# hsize = int((float(imgDefaul.size[1]) * float(wpercent)))
# imgDefaul = imgDefaul.resize((basewidth, hsize), Image.ANTIALIAS)
# render = ImageTk.PhotoImage(imgDefaul)
# img1 = Label(root, image=render)
# img1.place(x=0, y=100)

root.mainloop()

