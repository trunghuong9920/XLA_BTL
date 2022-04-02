import cv2


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
    imageCrop = img [y:y+h, x:x+w]                                                #x, y của điểm trên bên trái của hình chữ nhật, 

    return img, thresh, imgDrawCt, imageCrop,imgContours

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    img, thresh, imgDrawCt, imageCrop,imgContours = Controller(frame)

    cv2.imshow("Default", img)
    cv2.imshow("DrawCt", imgDrawCt)
    cv2.imshow("imageCrop", imageCrop)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
