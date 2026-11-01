# 인증 정보 보호

## 커밋·push 전 검사

저장소 루트에서 한 번 설정합니다. Python 3이 필요합니다.

```powershell
git config core.hooksPath .githooks
```

`pre-commit`은 스테이징한 전체 파일을, `pre-push`는 모든 로컬 참조에서 도달 가능한 과거 기록을 검사합니다. 키가 삭제된 오래된 커밋도 검사하므로, 기존 기록을 다시 병합해서 인증 정보가 되살아나는 일을 탐지합니다. 값은 출력하지 않고 위치와 유형만 표시합니다. 검사를 완료할 수 없을 때도 커밋·push를 차단합니다.

수동 실행:

```powershell
python scripts/check_secrets.py --staged
python scripts/check_secrets.py --history
```

GitHub의 `Secret scan` 워크플로도 전체 기록과 Gitleaks 기본 규칙·추가 규칙을 검사합니다. Actions 검사는 push 후 실행됩니다. 로컬 훅은 새 clone마다 활성화해야 합니다. 패턴 검사는 지원하는 형식에 대한 보호이며, 모든 민감 정보의 부재를 보장하지는 않습니다.

## 과거 기록 정리 후

과거 키와 출력된 키 일부를 제거하면 해당 커밋과 그 후손의 SHA가 변경됩니다. 공동 작업자는 새로 clone하는 것이 안전합니다. 이전 브랜치·태그·백업을 다시 push하거나 병합하면 원래 기록이 재유입될 수 있습니다.

기록에서 삭제한 키도 각 서비스에서 폐기·재발급해야 합니다. GitHub의 과거 PR 참조·캐시, 다른 사람의 clone·fork는 브랜치 재작성만으로 없어지지 않습니다. PR 참조와 캐시 정리가 필요한 경우 [GitHub 민감 정보 제거 절차](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)에 따라 지원팀에 요청하세요.

정리 전 백업과 상세 검사 결과는 이 저장소 밖에 보관합니다. 실제 키를 담은 백업을 공개 저장소에 올리지 마세요.
