---
name: unreal-run-skill
description: |
  Unreal Engine 에디터 실행, 커맨드렛, PIE 등을 지원합니다.
  "에디터 실행", "커맨드렛", "PIE" 등의 키워드에서 활성화됩니다.
context: fork
agent: unreal-run-agent
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Unreal Run Skill

실행 관련 작업을 독립 컨텍스트에서 실행합니다.

## 활성화 키워드

- 에디터 실행, 에디터 열어줘, open editor
- 커맨드렛, commandlet, -run=
- PIE, Play In Editor, 게임 실행
- 쿠킹, cooking, 패키징, packaging

## 에디터 실행

사용자가 "에디터 실행해줘", "에디터 열어줘" 등을 요청하면:
→ 에디터 실행 명령 수행

상세: [EDITOR.md](./EDITOR.md)

## 커맨드렛 실행

사용자가 특정 커맨드렛 실행을 요청하면:
→ 커맨드렛 명령 수행

상세: [COMMANDLET.md](./COMMANDLET.md)

## PIE 실행

사용자가 "게임 테스트해줘", "PIE 실행해줘" 등을 요청하면:
→ PIE 모드로 에디터 실행

## 쿠킹/패키징

사용자가 "쿠킹해줘", "패키징해줘" 등을 요청하면:
→ 쿠킹 또는 패키징 명령 수행
