import cv2

# 이미지 읽기
img_path = ""
image = cv2.imread(img_path, cv2.IMREAD_COLOR)
if image is None:
    raise Exception("Error: Unable to read the image file.") # 예외 처리


x_axis =                  # x축 기준 상하 뒤집기
y_axis =                  # y축 기준 좌우 뒤집기
xy_axis = 
rep_image   =        # 반복 복사
trans_image =           # 행렬 전치

## 각 행렬을 영상으로 표시
titles = ['image', 'x_axis', 'y_axis','xy_axis','rep_image','trans_image']
for title in titles:
    cv2.imshow(title, eval(title))
cv2.waitKey(0)