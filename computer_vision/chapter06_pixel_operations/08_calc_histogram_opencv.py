import numpy as np, cv2

image = cv2.imread("chapter06_pixel_operations/images/pixel.jpg", cv2.IMREAD_GRAYSCALE) # 영상 읽기
if image is None: raise Exception("영상 파일 읽기 오류 발생")

hsize, ranges = [32], [0, 256]                  # 히스토그램 간격수, 값 범위
hist_opencv = cv2.calcHist([image],[0],None,hsize,ranges)
# 히스토그램 출력
print("OpenCV 함수: \n", hist_opencv.flatten())                # 행렬을 벡터로 변환하여 출력

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()