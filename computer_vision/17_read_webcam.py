import cv2

def display_info(frame, text, pt, value, color=(120, 200, 90)): 
    text += str(value)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, pt, font, 0.7, color, 2)


capture = cv2.VideoCapture(0)  # 0번 카메라 연결
if capture.isOpened() == False:
    raise Exception("카메라 연결 안됨")

# 카메라 속성 획득 및 출력
print("너비 %d" % capture.get(cv2.CAP_PROP_FRAME_WIDTH))
print("높이 %d" % capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("노출 %d" % capture.get(cv2.CAP_PROP_EXPOSURE))
print("밝기 %d" % capture.get(cv2.CAP_PROP_BRIGHTNESS))


negative_mode = False

while True:  # 무한 반복
    ret, frame = capture.read()
    if not ret: break

    key = cv2.waitKey(30)
    if key >= 0 and key != ord('n'): # n키가 아닌 키를 누르면 종료
        break
    elif key == ord('n'): # n키를 누르면 네거티브 모드 토글ㅜ
        negative_mode = not negative_mode

    if negative_mode:
        frame = cv2.bitwise_not(frame) # 색상 반전 (네거티브 효과)

    exposure = capture.get(cv2.CAP_PROP_EXPOSURE)
    display_info(frame, "EXPOSURE: ", (10, 40), exposure)
    
    title = "View Frame from Camera"
    cv2.imshow(title, frame)
      # 윈도우에 영상 띄우기
capture.release()
cv2.destroyAllWindows()