---
name: update-plugin
description: rekah-plugins 마켓플레이스와 플러그인 캐시를 업데이트합니다
---

# Update Plugin Command

Git 기반 마켓플레이스 플러그인의 2중 캐시 문제를 해결하기 위해 업데이트를 수행합니다.

> **배경**: Git 마켓플레이스 플러그인은 `marketplaces/` (Git clone)와 `cache/` (런타임 복사본) 2중 구조를 사용합니다. 버전을 범프해도 명시적인 업데이트 없이는 캐시가 갱신되지 않습니다.

## 사용법

```
/rekah-unreal:update-plugin
```

## 동작

이 커맨드가 실행되면 다음 단계를 순서대로 수행하세요:

### Step 1: 마켓플레이스 업데이트 (Git Pull)

```bash
claude plugin marketplace update rekah-plugins
```

이 명령은 `~/.claude/plugins/marketplaces/rekah-plugins/`에서 `git pull`을 수행합니다.

### Step 2: 플러그인 재설치 (캐시 갱신)

```bash
claude plugin uninstall rekah-unreal@rekah-plugins
claude plugin install rekah-unreal@rekah-plugins --scope project
```

이 명령은 업데이트된 파일을 `marketplaces/`에서 `cache/`로 새 버전과 함께 복사합니다.

### Step 3: Claude Code 재시작

```
exit
claude
```

새 플러그인 버전을 로드하려면 세션을 재시작해야 합니다.

## 예상 결과

```
✅ 마켓플레이스 업데이트 완료 (git pull)
✅ 플러그인 재설치 완료 (예: 0.2.0 → 0.3.0)
⚠️  Claude Code를 재시작해주세요 (exit → claude)
```

## 캐시 구조

```
~/.claude/plugins/
├── marketplaces/rekah-plugins/    # Git clone (원본)
│   └── plugins/rekah-unreal/
│       └── .claude-plugin/plugin.json
│
└── cache/rekah-plugins/rekah-unreal/   # 런타임용 복사본
    ├── 0.1.0/  ← .orphaned_at 파일로 비활성화 표시
    └── 0.2.0/  ← 현재 활성 버전
```

## 문제 해결

### 업데이트 후에도 변경사항이 안 보이는 경우

1. 마켓플레이스 버전 확인:
   ```bash
   cat ~/.claude/plugins/marketplaces/rekah-plugins/plugins/rekah-unreal/.claude-plugin/plugin.json
   ```

2. 캐시 버전 확인:
   ```bash
   ls ~/.claude/plugins/cache/rekah-plugins/rekah-unreal/
   ```

3. 세션 재시작 확인

### 강제 클린 업데이트 (최후의 수단)

```powershell
# PowerShell - 모든 캐시 삭제
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache\rekah-plugins"
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\marketplaces\rekah-plugins"

# 처음부터 재설치
claude plugin install rekah-unreal@rekah-plugins --scope project
```

## 참고 문서

- [plugin-update-guide.md](../../../docs/rekah-plugins/basic_skills/plugin-update-guide.md)
