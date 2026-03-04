import cv2

# 이미지 읽기
image_path = "images/read_color.jpg"
image = cv2.imread(image_path, cv2.IMREAD_COLOR)
if image is None:
    raise Exception("Error: Unable to read the image file.") # 예외 처리
if image.ndim != 3:
    raise Exception("Error: The image is not a color image.") # 컬러 영상인지 확인
    
# 채널 분리
blue_channel = image[:,:,0]
green_channel = image[:,:,1]
red_channel = image[:,:,2]

# 자료형 체크 및 정보 출력
print("blue_channel 자료형:",type(blue_channel), blue_channel.dtype )
print("green_channel 자료형:",type(green_channel), green_channel.dtype )
print("red_channel 자료형:", type(red_channel), red_channel.dtype)

# 각 채널을 윈도우에 띄우기 
cv2.imshow("Original Image", image)
cv2.imshow("Blue Channel", blue_channel) # Blue 채널
cv2.imshow("Green Channel", green_channel) # Green 채널
cv2.imshow("Red Channel", red_channel) # Red 채널

cv2.waitKey()
cv2.destroyAllWindows()