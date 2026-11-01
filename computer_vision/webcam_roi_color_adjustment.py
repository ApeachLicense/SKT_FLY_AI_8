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



# 관심 영역(ROI) 설정: x=200, y=100, w=100, h=200
x, y, w, h = 200, 100, 100, 200

while True:  # 무한 반복
    ret, frame = capture.read()
    if not ret: break

    # 1. 관심 영역(ROI) 녹색 성분 증가
    # 영상 데이터에 직접 접근하여 수정 (split/merge 불필요)
    roi_g = frame[y:y+h, x:x+w, 1]
    # cv2.add의 결과를 roi_g에 직접 할당(dst 파라미터 사용)하면 메모리 불연속 문제로 에러 발생 가능
    # 따라서 결과를 따로 계산한 뒤에 슬라이스에 덮어쓰기 합니다.
    roi_g[:] = cv2.add(roi_g, 50)

    # 2. 테두리 그리기 (빨간색, 두께 3)
    # rectangle(영상, 시작좌표, 종료좌표, 색상, 두께)
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)

    cv2.imshow("ex16", frame)
    if cv2.waitKey(30) >= 0: break # delay 대신 30ms 사용
      
capture.release()
cv2.destroyAllWindows()