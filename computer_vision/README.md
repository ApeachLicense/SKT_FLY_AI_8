# 컴퓨터 비전 실습

| 경로 | 내용 |
| --- | --- |
| 폴더 루트의 `.py` | OpenCV 창, 그리기, 영상 읽기, 카메라 입문 |
| `chapter05_arrays/` | 영상 배열, 채널, 산술·비트 연산 |
| `chapter06_pixel_operations/` | 화소, 밝기, 대비, 히스토그램, 색 공간 |
| `chapter07_filters_and_morphology/` | 블러, 경계 검출, 필터, 형태학 연산 |
| `chapter08_geometric_transforms/` | 확대·축소, 이동, 어파인·원근 변환 |
| `chapter13_motion_and_landmarks/` | 광류, 얼굴·손·포즈 랜드마크 |
| `Common/` | 예제가 공유하는 보조 함수; 기존 import 경로 유지 |
| `deep_learning_review/` | 딥러닝 수업 복습 노트북 |
| `image_classification.ipynb` | 이미지 분류 노트북 |
| `yolo_openvino_person_mosaic.py` | YOLO·OpenVINO로 사람 영역 모자이크 |

## 실행 경로

기존 예제의 상대 경로를 위해 `computer_vision`을 작업 폴더로 사용하세요. 예를 들어 저장소 루트에서:

```powershell
cd computer_vision
python chapter07_filters_and_morphology/01_blurring.py
```

일부 예제는 스크립트가 있는 폴더의 `images/` 또는 동영상 파일을 기준으로 작성되어 있습니다. 파일을 찾지 못하면 해당 스크립트의 상대 경로와 실행 폴더를 확인하세요. 원래 자료에 없는 입력 영상은 별도로 준비해야 합니다. 카메라 예제는 로컬 웹캠과 GUI 환경이 필요합니다.

## 미완성 학습 예제

아래 6개 파일은 정리 이전부터 문법 오류 또는 빈칸이 있던 학습 자료입니다. 이름·경로를 정리하면서 원래 과제 내용을 보존했으며, 실행하려면 먼저 완성해야 합니다.

- `01_mat_array.py`
- `03_image_channels.py`
- `chapter07_filters_and_morphology/15_dilate.py`
- `chapter13_motion_and_landmarks/07_face_mesh_exercise.py`
- `chapter13_motion_and_landmarks/08_hand_landmarks_exercise.py`
- `chapter13_motion_and_landmarks/09_pose_landmarks_exercise.py`

`archives/`의 프로젝트 ZIP과 `yolov8n_openvino_model/`의 생성 모델은 로컬에 보존하고 Git에서는 제외합니다. 모델 생성 예제는 실행 시 필요한 가중치를 내려받거나 변환할 수 있습니다.
