# GitHub 공개 전 확인

파일 이름을 바꾸거나 최신 커밋에서 키를 삭제해도 과거 Git 기록은 남습니다. 이 저장소에서 발견된 과거 인증 키를 먼저 폐기·재발급하고, 기록 정리와 재검사를 마친 뒤 공개하세요. [GitHub 민감 정보 제거 안내](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)를 참고하세요.

## 로컬 변경 검토

이름 정리 전에 이미 존재하던 이동·삭제 작업도 현재 작업 폴더에 포함되어 있습니다. 특히 아래 명령은 그 변경까지 함께 스테이징하므로 내용을 먼저 확인하세요.

```powershell
git status --short
git add -A
git diff --cached --stat
git diff --cached --name-status
```

실제 키가 diff에 포함될 수 있으므로 전체 diff나 검사 결과 원문을 공개 채널에 붙이지 마세요. `.gitignore`는 이미 커밋된 파일이나 과거 커밋을 삭제하지 않습니다. 제외 자료가 커밋에 다시 포함되지 않았는지도 확인하세요.

## 공개 전에 남은 작업

1. 기존 Azure Storage·Image Analysis 및 OpenAI 키를 서비스에서 폐기·재발급합니다. 새 키는 로컬 환경이나 배포 서비스의 비밀 저장소에만 입력합니다.
2. 별도의 백업을 보관한 후, `git-filter-repo` 등으로 영향을 받는 모든 브랜치·태그의 인증 정보와 공개에서 제외할 자료를 정리합니다. 강제 푸시는 공동 작업자의 기존 기록에 영향을 주므로 범위를 합의한 뒤 수행합니다.
3. 새로 clone한 복사본에서 비밀 정보가 다시 탐지되지 않는지 확인합니다. PR·이슈·Actions 로그·첨부 파일은 Git 파일 검사와 별도로 확인합니다.
4. 강의 자료, 이미지, 동영상 및 외부 예제의 출처·재배포 조건을 확인합니다. 라이선스는 본인에게 권한이 있는 코드에 대해서만 선택합니다.
5. 공개할 커밋이 원격 저장소에 반영되었는지 확인한 뒤 GitHub 저장소의 **Settings → General → Danger Zone → Change repository visibility → Change to public**에서 변경합니다.

공개 전환 시 기록과 Actions 로그의 공개 범위도 달라집니다. 최종 화면의 안내는 [GitHub 공개 범위 문서](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility)를 확인하세요.
