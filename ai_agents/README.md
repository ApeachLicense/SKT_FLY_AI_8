# AI 에이전트 실습

노트북은 LCEL → RAG → 구조화된 출력 → LangGraph → 도구 → 메모리 → 데이터베이스 메모리 → 커스텀 RAG → 감독 에이전트 순서로 정리했습니다. `10_mcp/`에는 MCP 서버와 클라이언트 예제가 있습니다.

```powershell
# 저장소 루트에서
python -m pip install -r ai_agents/requirements.txt
Copy-Item .env.example .env
# .env에서 사용할 서비스의 키를 설정한 뒤
python -m jupyterlab
```

기존 `requirements.txt`는 기본 패키지 목록입니다. 개별 실습에서 사용하는 추가 패키지와 외부 데이터는 각 노트북에 맞게 준비해야 합니다. API 호출에는 사용 중인 계정의 요금이 발생할 수 있습니다.

키 확인 셀은 값 대신 설정 여부만 표시합니다. 공유하기 전에는 저장된 출력에 인증 정보나 개인 데이터가 포함되지 않았는지 확인하세요.

`stages/`는 음성 처리, 특징·의도 추출, 자막, 햅틱 변환을 위한 별도 모듈 모음입니다. 이 폴더의 함수명과 import 경로는 유지했습니다.
