import numpy as np, cv2


image = cv2.imread("chap07/images/morph.jpg", cv2.IMREAD_GRAYSCALE)
if image is None: raise Exception("영상파일 읽기 오류")

mask = np.array([[0, 1, 0],                         # 마스크 초기화
                 [1, 1, 1],
                 [0, 1, 0]]).astype("uint8")

th_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)[1]

dst2 = cv2.morphologyEx(th_img;)
# dst2 = cv2.dilate(th_img, mask)

cv2.imshow("OpenCV dilate", dst2)
cv2.waitKey(0)