import cv2 as cv
import mediapipe as mp

mp_mesh=mp.solutions.face_mesh
mp_drawing=mp.solutions.drawing_utils
mp_styles=mp.solutions.drawing_styles

mesh=mp_mesh.FaceMesh(         )

cap=cv.VideoCapture(0,cv.CAP_DSHOW)

while True:
    ret,frame=cap.read()
    if not ret:
      print('프레임 획득에 실패하여 루프를 나갑니다.')
      break
    
    res=mesh.process(cv.cvtColor(frame,cv.COLOR_BGR2RGB))
    
    if res.multi_face_landmarks:
        for landmarks in res.multi_face_landmarks:
            

            
    cv.imshow('MediaPipe Face Mesh',cv.flip(frame,1))		# 좌우반전
    if cv.waitKey(5)==ord('q'):
      break

cap.release()
cv.destroyAllWindows()