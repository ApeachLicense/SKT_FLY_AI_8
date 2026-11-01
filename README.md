# SKT FLY AI 8 — 학습 기록

Python, 딥러닝, 컴퓨터 비전, AI 에이전트, Azure 실습을 주제별로 정리한 저장소입니다. 각 폴더는 독립적인 예제 모음이며, 하나의 애플리케이션으로 실행하는 구조는 아닙니다.

| 폴더 | 내용 |
| --- | --- |
| [python_basics](python_basics/) | Python, HTTP 요청, MySQL, Streamlit 예제 |
| [deep_learning](deep_learning/) | PyTorch 텐서, 자동 미분, CNN·ResNet·ViT, Grad-CAM 과제 |
| [computer_vision](computer_vision/) | OpenCV 영상 처리, 광류, MediaPipe, YOLO·OpenVINO 실습 |
| [OpenVINO-Gaze-Tracker-main](OpenVINO-Gaze-Tracker-main/) | OpenVINO 기반 시선 추적·얼굴 속성 분석 프로젝트 |
| [ai_agents](ai_agents/) | LangChain, RAG, LangGraph, 메모리, MCP 및 오디오 처리 단계 |
| [cloud_azure](cloud_azure/) | Azure Blob Storage, 이미지 분석, Express, Functions, Git 시각화 |

## 시작하기

사용할 예제의 폴더에서 의존성을 설치하세요. 딥러닝 모델·데이터 다운로드, 외부 API 호출, 카메라 접근은 예제별로 필요합니다.

```powershell
# 저장소 루트에서 Python 환경 생성
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Streamlit 숫자 맞히기 예제
python -m pip install streamlit
python -m streamlit run python_basics/streamlit_examples/number_guessing_game.py
```

노트북은 JupyterLab에서 엽니다.

```powershell
python -m pip install jupyterlab
python -m jupyterlab
```

각 노트북이 사용하는 패키지는 해당 실습 환경에 추가로 설치해야 합니다. AI 에이전트 실습은 [별도 안내](ai_agents/README.md)를 참고하세요.

## 인증 정보

필요한 경우 `.env.example`을 `.env`로 복사하고 자신의 값을 입력하세요. `ai_agents` 예제는 `python-dotenv`로 이 파일을 읽습니다. Azure Python 예제는 운영체제 환경변수를 사용합니다. 설정 방법은 [Azure 안내](cloud_azure/README.md)에 있습니다.

`.env`, Azure 로컬 설정, 캐시, 다운로드한 모델, 편집기 설정은 Git에서 제외합니다. API 키를 코드·노트북 셀·출력에 직접 넣지 마세요.

커밋·push 전 검사를 활성화하려면 `git config core.hooksPath .githooks`를 실행하세요. GitHub에서도 전체 기록을 검사합니다. 설정과 기록 정리 후 주의 사항은 [인증 정보 보호 안내](docs/secret-protection.md)를 참고하세요.

## 학습 자료와 미완성 예제

일부 OpenCV 파일은 빈칸을 채우는 학습용 예제로, 실행 전에 수정이 필요합니다. 목록과 실행 경로는 [컴퓨터 비전 안내](computer_vision/README.md)에 있습니다. 비전 폴더의 딥러닝 복습본은 원래 자료 구성을 보존한 사본입니다.

강의 PDF, 보고서 원본, 프로젝트 ZIP은 로컬 참고 자료로 보존하며 새 커밋에서는 제외합니다. 이미지·동영상·외부 예제의 출처와 재배포 조건은 공개 전에 확인해야 합니다. 저장소 전체에 적용할 라이선스는 아직 지정하지 않았습니다.

파일 이름 변경 내역은 [경로 대응표](docs/path-changes.csv), 공개 전 절차는 [공개 안내](docs/publishing.md)를 참고하세요.
