import cv2
from cv2 import imread
from cv2 import waitKey
vidcap = cv2.VideoCapture('vd1.mp4')
success, image = vidcap.read()
count = 1

while success:
    if cv2.imread("video_data/image_%d.jpg" %count) is None:
        cv2.imwrite("video_data/image_%d.jpg" % count, image)    
        # img = imread("video_data/image_%d.jpg" %count)
        # cv2.imshow("img",img)

    success, image = vidcap.read()
    print('Image video_data/image_%d.jpg', count)
    count += 1

waitKey()