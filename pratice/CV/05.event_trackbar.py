from email.charset import add_charset
import numpy as np
import cv2

def onChange(value):												# 트랙바 콜백 함수
    global image                        	# 전역 변수 참조

    add_value = value - int(image[0][0])
    print("추가 화소값:",add_value)

    # uint8 연산 오버플로우 방지를 위해 int로 변환 후 연산
    image[:] = np.clip(image.astype(int) + add_value, 0, 255).astype(np.uint8)
    cv2.imshow(title, image)

image = np.zeros((400,600), np.uint8)     	# 영상 생성

title = 'Trackbar Event'
cv2.imshow(title, image)

cv2.createTrackbar("Brightness", title, image[0][0], 255, onChange)	# 트랙바 콜백 함수 등록
cv2.waitKey(0)
cv2.destroyAllWindows()