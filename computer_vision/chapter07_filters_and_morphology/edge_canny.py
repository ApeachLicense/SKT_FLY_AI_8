import numpy as np, cv2

def onTrackbar(x):
    th1 = cv2.getTrackbarPos('Threshold1','Canny Edge')
    th2 = cv2.getTrackbarPos('Threshold2','Canny Edge')

    edge_image = cv2.Canny(image, th1, th2)
    cv2.imshow('Canny Edge', edge_image)

image = cv2.imread("chapter07_filters_and_morphology/images/canny.jpg",cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("Image load failed")

cv2.imshow("Canny Edge",image)
cv2.createTrackbar('Threshold1','Canny Edge',50,255,onTrackbar)
cv2.createTrackbar('Threshold2','Canny Edge',150,255, onTrackbar)

# 초기 실행 (getTrackbarPos 오류 방지를 위해 직접 호출)
edge_image = cv2.Canny(image, 50, 150)
cv2.imshow('Canny Edge', edge_image)
cv2.waitKey(0)