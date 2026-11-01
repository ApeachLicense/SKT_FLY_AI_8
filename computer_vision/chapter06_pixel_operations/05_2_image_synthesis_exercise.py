import numpy as np, cv2

image1 = cv2.imread("chapter06_pixel_operations/images/add1.jpg", cv2.IMREAD_GRAYSCALE)   # 영상 읽기
image2 = cv2.imread("chapter06_pixel_operations/images/add2.jpg", cv2.IMREAD_GRAYSCALE)
if image1 is None or image2 is None: raise Exception("영상 파일 읽기 오류 발생")

def onChange(val):
    alpha = cv2.getTrackbarPos('Alpha', 'concatenated image') / 100
    beta = cv2.getTrackbarPos('Beta', 'concatenated image') / 100
    
    add_img3 = cv2.addWeighted(image1, alpha, image2, beta, 0)
    
    result = cv2.hconcat([image1, add_img3, image2])
    cv2.imshow("concatenated image", result)

cv2.imshow("concatenated image", image1) # 초기 윈도우 생성
cv2.createTrackbar('Alpha', 'concatenated image', 50, 100, onChange)
cv2.createTrackbar('Beta', 'concatenated image', 50, 100, onChange)

onChange(0) # 초기 실행
cv2.waitKey(0)