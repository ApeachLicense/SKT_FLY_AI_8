# OpenVINO Gaze Estimation Project

이 프로젝트는 Intel OpenVINO 툴킷을 활용하여 실시간 **시선 추적(Gaze Estimation)** 및 **얼굴 속성 분석(나이/성별/감정)** 시스템을 구현한 결과물입니다.
**Intel Core Ultra 프로세서(NPU 탑재)**와 **Intel Arc 그래픽(GPU)**의 하드웨어 가속을 적극 활용하여 고성능 파이프라인을 구축했습니다.

## 1. 프로젝트 주요 기능
- **얼굴 감지 (Face Detection)**: `MobileNet-SSD` 기반의 고속 얼굴 탐지
- **랜드마크 추출 (Landmarks)**: 눈, 코, 입 등 35개 주요 포인트 인식
- **머리 각도 추정 (Head Pose)**: Yaw, Pitch, Roll 3축 각도 계산
- **시선 추적 (Gaze Estimation)**: 눈 이미지와 머리 각도를 결합하여 시선 벡터 추적
- **속성 분석**: 나이, 성별, 5가지 감정(행복, 슬픔 등) 실시간 분석

## 2. 사용된 AI 모델 (Open Model Zoo)
인텔의 Open Model Zoo에서 제공하는 경량화(Lightweight) 및 최적화된 모델(`FP16`)을 사용했습니다.

| 기능 | 모델명 | 설명 |
| :--- | :--- | :--- |
| **얼굴 감지** | `face-detection-adas-0001` | ADAS용으로 최적화된 고속 탐지 모델 |
| **랜드마크** | `facial-landmarks-35-adas-0002` | 가벼운 CNN 기반 35포인트 추출기 |
| **머리 각도** | `head-pose-estimation-adas-0001` | 회귀(Regression) 방식의 각도 추정기 |
| **시선 추적** | `gaze-estimation-adas-0002` | Multi-stream CNN (눈+머리 정보 융합) |
| **나이/성별** | `age-gender-recognition-retail-0013` | Multi-task CNN (분류+회귀) |
| **감정 분석** | `emotions-recognition-retail-0003` | 5개 클래스 분류기 |

## 3. 하드웨어 가속 및 최적화 (Benchmark)

본 프로젝트는 `benchmark.py` 스크립트를 통해 시스템에 장착된 **CPU, GPU, NPU**의 성능을 비교 분석하고, 최적의 장치를 자동으로 선정했습니다.

### 📊 벤치마크 결과 (기기: Intel Core Ultra 7 256V / Arc 140V)
100 프레임 추론 테스트 결과입니다.

| 장치 (Device) | 성능 (Avg FPS) | 비고 |
| :--- | :--- | :--- |
| **CPU** | **63.16 FPS** | 준수함 (Intel Core Ultra 7) |
| **GPU** | **139.90 FPS** 🏆 | **최고 성능** (Intel Arc 140V) |
| **NPU** | **44.12 FPS** | 전력 효율 중심 (Intel AI Boost) |

### 🚀 최적화 결론
가장 높은 성능을 보인 **GPU (Intel Arc 140V)**를 메인 추론 장치로 선정하여, 복잡한 파이프라인(6개 모델 동시 구동)에서도 **Average 140 FPS**라는 경이적인 실시간 성능을 확보했습니다.

## 4. 실행 방법

이 폴더에서 의존성을 설치한 뒤 실행합니다.

```bash
python -m pip install -r requirements.txt
```

다운로드한 `models/intel/`의 모델 파일과 자동 생성되는 `first.txt`는 Git에서 제외합니다. 로컬 모델은 그대로 보존되어 있습니다. 새로 clone한 환경에서는 Open Model Zoo 다운로더로 위 표의 6개 모델을 준비하세요.

```bash
omz_downloader --name face-detection-adas-0001,facial-landmarks-35-adas-0002,head-pose-estimation-adas-0001,gaze-estimation-adas-0002,age-gender-recognition-retail-0013,emotions-recognition-retail-0003 --precisions FP16 --output_dir models
```

기본 실행 장치는 `main.py`의 `DEVICE = "GPU"`입니다. GPU가 없는 환경에서는 사용 가능한 장치에 맞춰 변경하세요. 모델은 [Intel Open Model Zoo](https://github.com/openvinotoolkit/open_model_zoo)에서 제공하며 각 모델의 사용 조건을 확인하세요.

### 기본 실행 (Main Pipeline)
웹캠을 통해 실시간 데모를 실행합니다.
```bash
python main.py
```

### 벤치마크 실행 (Performance Test)
내 하드웨어에서 각 장치별 성능을 테스트합니다.
```bash
python benchmark.py
```

### 모델 정보 기록 (Log)
현재 사용 중인 모델의 상세 정보를 `first.txt`로 저장합니다.
```bash
python record_model_info.py
```
