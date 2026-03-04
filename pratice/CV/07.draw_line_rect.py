import numpy as np
import cv2

yellow, cyan, magenta = (0, 255, 255), (255, 255, 0), (255, 0, 255)
image =  np.zeros((500,700,3), np.uint8 )
image[:] = (200, 200, 200)

pt1, pt2 = (100,100),(300,200)                  		        # 
pt3, pt4 = (500,200),(600,100)
roi = (100,300,300,150)

# 직선 그리기
cv2.line(image, pt1, pt2, cyan, 2, cv2.LINE_8)
cv2.line(image, pt3, pt4, magenta, 4, cv2.LINE_AA)    			# 

# 사각형 그리기
cv2.rectangle(image, pt1, pt2, yellow, 3, cv2.LINE_4)             # 
cv2.rectangle(image, roi, cyan, 3, cv2.LINE_8 )                  # 
cv2.rectangle(image, (500,300,150,200), magenta, cv2.FILLED )  # 내부 채움

cv2.imshow('Line & Rectangle', image)							# 
cv2.waitKey(0)
cv2.destroyAllWindows()											# 모든 열린 윈도우 닫기