import cv2
import os
import urllib.request
import time

def download_haarcascade_file():
    """Haarcascade 파일이 없으면 다운로드"""
    filename = "haarcascade_frontalface_default.xml"
    if os.path.exists(filename):
        return
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    print("Downloading Haarcascade XML...")
    urllib.request.urlretrieve(url, filename)
    print("Download complete:", filename)

def clip_bbox(x, y, w, h, W, H):
    """Bbox가 이미지 경계를 벗어나지 않도록 클리핑"""
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(W, x + w), min(H, y + h)
    if x2 <= x1 or y2 <= y1:
        return None
    return x1, y1, x2, y2

def pixelate_optimized(roi, blocks=10):
    """
    cv2.resize를 이용한 고속 픽셀화 (Nearest Neighbor Interpolation)
    - Downscale: 이미지를 뭉개서 정보 손실 유도
    - Upscale: Nearest Neighbor로 확대하여 격자 무늬 생성
    """
    h, w = roi.shape[:2]
    
    # 예외 처리: ROI가 너무 작으면 처리하지 않음
    if h < blocks or w < blocks:
        return roi

    # 1. 축소 (정보 압축)
    small = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
    
    # 2. 확대 (모자이크 효과 적용)
    # INTER_NEAREST: 인접 픽셀 값을 그대로 가져와서 '계단 현상(픽셀화)'을 만듦
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated

if __name__ == "__main__":
    download_haarcascade_file()

    # 설정값
    BLOCKS = 15  # 모자이크 격자 수 (가로, 세로 블록 개수)
    
    cap = cv2.VideoCapture(0)
    # 카메라 해상도 설정 (성능과 화질의 타협점, 필요시 조절)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    
    prev_time = 0  # FPS 계산용

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        H, W = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # 얼굴 탐지 (파라미터 튜닝)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,    # 1.1 -> 1.2 (탐색 속도 향상, 약간의 정확도 희생)
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            bbox = clip_bbox(x, y, w, h, W, H)
            if bbox is None:
                continue
            
            x1, y1, x2, y2 = bbox
            
            # ROI 추출 (NumPy Slicing은 메모리 복사가 아닌 뷰(View)를 생성하므로 빠름)
            face_roi = frame[y1:y2, x1:x2]
            
            # 최적화된 픽셀화 적용
            frame[y1:y2, x1:x2] = pixelate_optimized(face_roi, blocks=BLOCKS)

        # FPS 출력 (성능 모니터링)
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time
        
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Optimized Mosaic", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()