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
def Controller(img):
    gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)                               #Tạo một bức ảnh xám từ bức ảnh gốc
    gray = cv2.medianBlur (gray, 5)                                             #Giảm nhiễu

    thresh = cv2.adaptiveThreshold (gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)                 #Lấy ảnh ngưỡng
    contours, h = cv2.findContours (thresh, 1,2)  


    imgContours = img.copy()
    if len(contours) > 0:
        cv2.drawContours(imgContours, contours,-1, (0, 255, 0),1)                  #Đánh dấu contours trên ảnh

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
                                                                                    #x, y của điểm trên bên trái của hình chữ nhật, 
    imageCrop = img.copy()
    cv2.drawContours(imageCrop, [largest_rectangle[1]],0, (255, 255, 255),8)          #Đánh dấu vùng contours vừa tìm được

    imageCrop = imageCrop[y:y+h, x:x+w] 
    return img, thresh, imgDrawCt, imageCrop,imgContours


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


def getImage():
    filetypes = (
        ('text files', '*.jpg'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != '':
        img = cv2.imread(filename)
        img, thresh, imgDrawCt, imageCrop, imgContours = Controller(img)
        cv2.imshow ('Default', img)
        # cv2.imshow ('Thresh', thresh)
        cv2.imshow ('Img Draw Max Contours', imgDrawCt)
        cv2.imshow ('imageCrop', imageCrop)
        # cv2.imshow("imgContours", imgContours)
        data = predict(imageCrop)
        label_show.set(data)

def getVideo():
    filetypes = (
        ('text files', '*.mp4'),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename != '':
        cap = cv2.VideoCapture(filename)

        while True:
            ret, frame = cap.read()

            img, thresh, imgDrawCt, imageCrop,imgContours = Controller(frame)

            cv2.imshow("Default", img)
            cv2.imshow("DrawCt", imgDrawCt)
            cv2.imshow("imageCrop", imageCrop)
            data = predict(imageCrop)
            print(data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
def getCamera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        img, thresh, imgDrawCt, imageCrop,imgContours = Controller(frame)

        cv2.imshow("Default", img)
        cv2.imshow("DrawCt", imgDrawCt)
        cv2.imshow("imageCrop", imageCrop)
        data = predict(imageCrop)
        print(data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def close():
    sys.exit()

root =Tk()
root.geometry("600x500")
root.option_add("*Font","TimeNewRoman 14")
label_show=StringVar()

Label (root, text="Nhận diện biển số xe máy với opencv và pytesseract").grid(row=0,columnspan=2)
Button (root, text="Chọn ảnh",bg= 'cyan', command=getImage).grid(row=3,column=0,padx=10,pady=10,sticky = W)
Button (root, text="Nhận diện video",bg= 'cyan', command=getVideo).grid(row=4,column=0,padx=10,pady=10,sticky = W)
Button (root, text="Nhận diện Camera",bg= 'cyan', command=getCamera).grid(row=5,column=0,padx=10,pady=10,sticky = W)
Button (root, text="Thoát",bg= 'cyan', command=close).grid(row=6,column=0,padx=10,pady=10,sticky = W)

Label (root, text="Kết quả:").grid(row=1,column=0,padx=10,pady=10,sticky = W)
Label(root,textvariable=label_show).grid(row=2,column=0,padx=10,pady=10,sticky = W)

# basewidth = 300
# imgDefaul = 'img_car/img1.jpg'
# imgDefaul= Image.open(imgDefaul)
# wpercent = (basewidth / float(imgDefaul.size[0]))
# hsize = int((float(imgDefaul.size[1]) * float(wpercent)))
# imgDefaul = imgDefaul.resize((basewidth, hsize), Image.ANTIALIAS)
# render = ImageTk.PhotoImage(imgDefaul)
# img1 = Label(root, image=render)
# img1.place(x=0, y=100)

root.mainloop()
