# Azure 및 웹 실습

| 폴더 | 내용 |
| --- | --- |
| `blob-storage/` | 로컬 파일을 Azure Blob Storage로 업로드 |
| `image-analysis/` | Azure Image Analysis로 이미지 분석 |
| `express-blog-app/` | Express·EJS 블로그 예제 |
| `guestbook/` | Azure Functions 방명록 |
| `git-history-visualizer/` | Git 로그 시각화 실험; `backend/`, `frontend/` |
| `python-http-sample/` | Requests HTTP 요청 예제 |

## Azure Python 예제

API 인증 정보는 운영체제 환경변수에서 읽습니다. 실제 값은 PowerShell 세션 등 로컬 환경에서만 설정하세요.

Blob Storage 예제는 `AZURE_STORAGE_CONNECTION_STRING`과 `AZURE_STORAGE_CONTAINER`가 필요합니다.

```powershell
python -m pip install azure-storage-blob
python cloud_azure/blob-storage/upload_blob.py ./sample.png --container YOUR_CONTAINER
```

이미지 분석 예제는 `AZURE_VISION_ENDPOINT`와 `AZURE_VISION_KEY`가 필요합니다.

```powershell
python -m pip install azure-ai-vision-imageanalysis Pillow
python cloud_azure/image-analysis/analyze_image.py
```

`.env.example`은 필요한 변수 이름을 안내합니다. Azure Python 예제에서 `.env` 파일을 자동으로 읽지는 않으므로 세션의 환경변수에 값을 설정해야 합니다.

## 웹 예제

각 프로젝트의 폴더에서 `npm ci`로 의존성을 설치합니다. Express 예제는 `npm start`, 방명록은 [별도 안내](guestbook/README.md)를 따릅니다. 방명록의 로컬 설정은 `local.settings.example.json`을 `local.settings.json`으로 복사해 준비합니다.

Git 시각화 프로젝트는 실험 중인 소스입니다. 폴더 이름은 `backend/`와 `frontend/`로 정리했으며, 기능 완성과 배포 검증은 별도 작업입니다.

강의 PDF와 보고서 원본은 `reference_materials/`에 로컬 자료로 보존하고 Git에서는 제외합니다. 제외 규칙만으로 이전 커밋의 자료가 없어지지는 않습니다.
