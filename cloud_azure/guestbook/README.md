# Azure Functions 방명록

**Azure Functions (Node.js v4)**, **Vanilla CSS**, **Docker**로 구축된 현대적인 서버리스 방명록 애플리케이션입니다.

## 주요 기능

- ⚡ **서버리스 백엔드**: Azure Functions (Node.js) 기반.
- 🎨 **프리미엄 UI**: 다크 모드와 글래스모피즘(Glassmorphism) 디자인이 적용된 깔끔한 UI.
- 🐳 **Docker 지원**: 컨테이너 배포 준비 완료.
- 💾 **인메모리 저장소**: 데모용 간편 데이터 저장 (휘발성).

## 프로젝트 구조

```
.
├── src
│   ├── functions       # Azure Functions 엔드포인트
│   │   ├── getMessages.js
│   │   ├── postMessage.js
│   │   └── frontend.js # 정적 자산(Static Assets) 서빙
│   ├── public          # 프론트엔드 자산 (HTML, CSS)
│   └── store.js        # 데이터 저장 로직
├── Dockerfile          # 컨테이너 설정
├── host.json           # Function 호스트 설정
└── package.json        # 의존성 패키지
```

## 시작하기

### 사전 요구 사항

- [Node.js](https://nodejs.org/) (v18 이상)
- [Azure Functions Core Tools](https://learn.microsoft.com/ko-kr/azure/azure-functions/functions-run-local)
- [Docker](https://www.docker.com/) (선택 사항)

### 로컬 개발

1.  **의존성 설치**:
    ```bash
    npm install
    ```

    `local.settings.example.json`을 `local.settings.json`으로 복사합니다. 기본값은 Azurite 로컬 저장소를 사용합니다. 실제 Azure 연결 문자열을 설정한 파일은 커밋하지 마세요.

2.  **애플리케이션 시작**:
    ```bash
    func start
    ```

3.  **방명록 접속**:
    브라우저에서 [http://localhost:7071](http://localhost:7071)을 엽니다.

### Docker 지원

컨테이너화된 애플리케이션 빌드 및 실행:

```bash
# 이미지 빌드
docker build -t guestbook .

# 컨테이너 실행 (http://localhost:8080 접속)
docker run -p 8080:80 guestbook
```

## API 엔드포인트

- `GET /api/messages`: 모든 방명록 메시지 조회.
- `POST /api/messages`: 새로운 메시지 작성.
  - Body: `{ "name": "이름", "message": "내용" }`
