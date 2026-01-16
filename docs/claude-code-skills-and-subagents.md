# Claude Code Skills와 Subagents 동작 가이드

Claude Code 플러그인에서 Skills와 Subagents의 context 전달, fork 동작, 상속 규칙 정리.

## SKILL.md 구조

```yaml
---
name: skill-name
description: 스킬 설명
context: fork          # 선택: subagent에서 실행
agent: agent-name      # 선택: 사용할 agent 지정
allowed-tools:         # 선택: 허용 도구 제한
  - Bash
  - Read
---

# 본문 (마크다운)
스킬 가이드라인 내용...
```

## context: fork 동작

| 설정 | 실행 위치 | Context 소모 | 용도 |
|------|-----------|--------------|------|
| `context: fork` 있음 | 별도 subagent | Main 미소모 | 빌드, 분석 등 대량 출력 |
| `context: fork` 없음 | Main conversation | Main 소모 | 간단한 가이드라인 |

### fork 사용 시 이점

- Subagent 출력은 별도 파일에 저장
- Main conversation에는 요약만 반환
- Main context 효율적 사용

## SKILL.md vs Agent MD

| 위치 | 내용 | 전달 대상 |
|------|------|-----------|
| SKILL.md | 활성화 조건, 간단한 설명 | Main context |
| Agent MD | 자세한 스펙, 사용법 | Subagent context |

**결론:** `context: fork` 사용 시 자세한 스펙은 **agent md**에 작성

### 예시: unreal-code-analysis

```
SKILL.md (간단)
  └── context: fork
  └── agent: unreal-code-analysis-agent
          ↓
unreal-code-analysis-agent.md (자세한 스펙 ~487줄)
  └── LSP 도구 사용법
  └── 커서 위치 계산법
  └── 예시 등
```

## Subagent와 Skills

### Skills 상속

**Subagent는 parent의 skills를 자동 상속받지 않음**

Subagent가 skills를 사용하려면 agent md에 명시:

```yaml
---
name: my-agent
skills: skill-a, skill-b
---
```

### 무한루프 방지

**"Subagent는 다른 subagent를 생성할 수 없다"**

| 호출 체인 | 가능 여부 |
|-----------|-----------|
| Main → Skill (fork) → Subagent | ✅ |
| Subagent → Skill (fork) → Subagent | ❌ |

구조적으로 depth 1로 제한되어 무한루프 불가.

## 플러그인 구조 권장 패턴

### 가이드라인 스킬 (fork 없음)

```
skills/
  └── python-coding/
      └── SKILL.md     # 가이드라인 직접 포함
```

Main context에서 실행, 코딩 규칙 참조용.

### 작업 위임 스킬 (fork 있음)

```
skills/
  └── unreal-build-skill/
      └── SKILL.md     # 간단한 설명 + context: fork + agent 지정

agents/
  └── unreal-build-agent.md   # 자세한 스펙
```

Subagent에서 실행, 대량 출력 작업용.

## 참고

- [Claude Code Skills 문서](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Claude Code Subagents 문서](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
