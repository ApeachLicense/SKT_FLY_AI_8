import numpy as np
import cv2

green, red, yellow = (0, 255, 0),(0, 0, 255),(0, 255, 255)
white = (255, 255, 255)

image = np.full((400, 800, 3), white, np.uint8)

pt1, pt2 = (200, 200), (600, 200) # 타원 중심점
size = (150, 80)                                        # 타원 크기 - 반지름 값임

cv2.circle(image, pt1, 1, 0, 2)                         # 타원의 중심점(2화소 원) 표시
cv2.circle(image, pt2, 1, 0, 2)






cv2.imshow("Draw Eclipse & Arc", image)
cv2.waitKey()                                           # 키입력 대기