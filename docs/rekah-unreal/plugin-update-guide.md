# Git-Based Marketplace Plugin Update Guide

> **생성일**: 2026-01-11
> **수정일**: 2026-01-11
> **버전**: 0.4.1
> **상태**: 검증 완료

---

## 현재 캐시 상태

| 위치 | 버전 | 상태 |
|------|------|------|
| **Marketplace** | `0.4.1` | ✅ 최신 |
| **Cache** | `0.4.1` | ✅ 활성 |

**구조**:
```
~/.claude/plugins/cache/rekah-plugins/rekah-unreal/
└── 0.4.1/           ← 현재 활성 버전
    ├── .claude-plugin/
    ├── agents/
    ├── commands/
    ├── scripts/
    └── skills/
```

---

## 개요

이 문서는 Claude Code가 Git 기반 마켓플레이스 플러그인을 어떻게 처리하는지, 그리고 올바른 업데이트 절차를 설명합니다.

---

## 문제 상황

Git 기반 마켓플레이스 플러그인에 변경사항을 푸시한 후, 다음 작업을 해도 Claude Code에 반영되지 않을 수 있습니다:
- `claude plugin uninstall && install` 실행
- Claude Code 세션 재시작

**근본 원인**: Git 기반 마켓플레이스 플러그인은 2중 캐시 시스템을 사용하며, 명시적인 업데이트 명령이 필요합니다.

---

## Claude Code 플러그인 디렉토리 구조

```
~/.claude/plugins/
├── marketplaces/           # 마켓플레이스 저장소의 Git clone
│   └── rekah-plugins/      # 커스텀 마켓플레이스 (Git clone)
│       └── plugins/
│           └── rekah-unreal/
│               └── .claude-plugin/plugin.json
│
└── cache/                  # Claude Code가 실제로 사용하는 캐시 복사본
    └── rekah-plugins/
        └── rekah-unreal/
            └── 0.4.1/      # 현재 활성 버전
```

### 핵심 인사이트

| 위치 | 용도 | 업데이트 트리거 |
|------|------|----------------|
| `marketplaces/` | 마켓플레이스 Git clone | `marketplace update` 명령 |
| `cache/` | 런타임용 버전별 복사본 | `plugin install` 명령 |

---

## 올바른 업데이트 절차

### 간편 업데이트 (권장)

```
/rekah-unreal:update-plugin
```

이 커맨드가 아래 절차를 안내합니다.

### 수동 업데이트

#### 1단계: 마켓플레이스 업데이트 (Git Pull)

```
claude plugin marketplace update rekah-plugins
```

이 명령은 `~/.claude/plugins/marketplaces/rekah-plugins/`에서 `git pull`을 수행합니다.

#### 2단계: 플러그인 재설치 (캐시 갱신)

```
claude plugin uninstall rekah-unreal@rekah-plugins
claude plugin install rekah-unreal@rekah-plugins --scope project
```

이 명령은 업데이트된 파일을 `marketplaces/`에서 `cache/`로 새 버전 번호와 함께 복사합니다.

#### 3단계: Claude Code 재시작

```
exit
claude
```

---

## 업데이트 흐름

```
GitHub Remote (0.5.0)
    ↓ ✅ 1단계: marketplace update (git pull)
Marketplace Clone (0.5.0)
    ↓ ✅ 2단계: plugin 재설치 (캐시로 복사)
Cache (0.5.0)
    ↓ ✅ 3단계: 세션 재시작
Claude Code가 신버전 로드
```

---

## 빠른 참조 명령어

### 전체 업데이트 시퀀스
```
# 1. 마켓플레이스 업데이트 (git pull)
claude plugin marketplace update rekah-plugins

# 2. 플러그인 재설치 (캐시 갱신)
claude plugin uninstall rekah-unreal@rekah-plugins
claude plugin install rekah-unreal@rekah-plugins --scope project

# 3. Claude Code 재시작
exit
claude
```

### 강제 클린 업데이트 (최후의 수단)

```powershell
# PowerShell - 모든 캐시 데이터 삭제
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\cache\rekah-plugins"
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\plugins\marketplaces\rekah-plugins"

# 그 후 처음부터 재설치
claude plugin install rekah-unreal@rekah-plugins --scope project
```

### 현재 캐시 상태 확인

```powershell
# 캐시된 버전 목록 확인
Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\rekah-plugins\rekah-unreal"

# 마켓플레이스 버전 확인
Get-Content "$env:USERPROFILE\.claude\plugins\marketplaces\rekah-plugins\plugins\rekah-unreal\.claude-plugin\plugin.json"
```

---

## 자동 업데이트 설정

기본적으로 **타사 마켓플레이스는 자동 업데이트가 비활성화**되어 있습니다.

마켓플레이스의 자동 업데이트를 활성화하려면:
1. Claude Code에서 `/plugin` 명령 실행
2. **Marketplaces** 탭으로 이동
3. 해당 마켓플레이스 선택
4. **Enable auto-update** 토글

활성화되면 Claude Code가 시작할 때 자동으로:
- 마켓플레이스 데이터 새로고침
- 설치된 플러그인을 최신 버전으로 업데이트

---

## 문제 해결

### 업데이트 후에도 플러그인 변경사항이 안 보이는 경우

1. 마켓플레이스가 업데이트되었는지 확인
2. 캐시가 업데이트되었는지 확인
3. 둘 다 구버전이면 전체 업데이트 시퀀스 실행

### SessionStart Hook이 실행되지 않는 경우

Windows에서 `.sh` 스크립트가 제대로 실행되지 않을 수 있습니다:
- PowerShell 스크립트(`.ps1`)로 변환 고려
- plugin.json에서 Python 직접 호출 고려

---

## 요약

| 작업 | 명령어 | 효과 |
|------|--------|------|
| 간편 업데이트 | `/rekah-unreal:update-plugin` | 절차 안내 |
| 마켓플레이스 업데이트 | `claude plugin marketplace update <이름>` | Git pull |
| 플러그인 재설치 | `claude plugin uninstall && install` | 캐시로 복사 |
| 강제 새로고침 | `cache/`와 `marketplaces/` 폴더 삭제 | 완전 초기화 |

**기억하세요**: Git 기반 마켓플레이스 플러그인의 경우, 버전 범프만으로는 충분하지 않습니다. 반드시 마켓플레이스를 명시적으로 업데이트해야 Git pull이 트리거됩니다.

---

## 변경 이력

| 날짜 | 변경 사항 |
|------|-----------|
| 2026-01-11 | v0.4.1 기준으로 문서 전면 업데이트, PowerShell 기반으로 변경 |
| 2026-01-11 | 초기 문서 작성 |
