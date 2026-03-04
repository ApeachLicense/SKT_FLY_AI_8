import cv2
import time
import numpy as np
from ultralytics import YOLO
from openvino.runtime import Core

# 1. OpenVINO 장치 확인
core = Core()
devices = core.available_devices
print(f"OpenVINO Devices: {devices}")

device_name = "CPU"
if "NPU" in devices:
    device_name = "NPU"
    print("Intel NPU Detected! Optimizing for Efficiency.")
elif "GPU" in devices:
    device_name = "GPU"
    print("Intel GPU (GPGPU) Detected! Using GPU for inference.")

# 2. YOLOv8 모델 로드 및 OpenVINO 변환
# PyTorch 모델 로드
pt_model = YOLO('yolov8n.pt') 

# OpenVINO 포맷으로 변환 (폴더가 없으면 자동 변환)
# half=True: FP16 반정밀도 사용 (GPU 속도 향상)
print("Checking/Exporting OpenVINO model...")
pt_model.export(format='openvino', half=True) 

# 변환된 OpenVINO 모델 로드
# Ultralytics는 폴더 경로를 넣으면 자동으로 OpenVINO 엔진을 사용함
ov_model = YOLO('yolov8n_openvino_model/')

def pixelate_optimized(roi, blocks=10):
    """이전 단계에서 최적화한 리사이징 방식의 모자이크"""
    h, w = roi.shape[:2]
    if h < blocks or w < blocks:
        return roi
    small = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 3. YOLO 추론 (OpenVINO)
        # device=device_name을 명시해도 Ultralytics OpenVINO 백엔드는 주로 AUTO/CPU로 동작하지만
        # half=True로 내보낸 모델을 사용하므로 가속 효과가 있음.
        results = ov_model.predict(frame, verbose=False, stream=True, classes=[0])

        for result in results:
            boxes = result.boxes
            for box in boxes:
                # OpenVINO 결과도 텐서/numpy 형태로 반환됨
                if box.xyxy.shape[1] == 4: # 박스 좌표가 있는 경우
                    coords = box.xyxy[0].cpu().numpy().astype(int)
                    x1, y1, x2, y2 = coords
                    
                    # 경계 처리
                    h, w = frame.shape[:2]
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)

                    # 사람 영역 모자이크
                    face_roi = frame[y1:y2, x1:x2]
                    frame[y1:y2, x1:x2] = pixelate_optimized(face_roi, blocks=15)

        # FPS 계산
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        # 정보 표시
        cv2.putText(frame, f"Backend: OpenVINO ({device_name})", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"FPS: {fps:.1f}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("YOLOv8 OpenVINO Mosaic", frame)

        if cv2.waitKey(1) == 27: # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()