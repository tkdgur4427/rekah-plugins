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

실행 관련 작업을 `unreal-run-agent`에 위임합니다.

## 활성화 키워드

- 에디터 실행, 에디터 열어줘, open editor
- 커맨드렛, commandlet, -run=
- PIE, Play In Editor, 게임 실행
- 쿠킹, cooking, 패키징, packaging

## 동작

1. 스킬 활성화 시 `unreal-run-agent` 호출
2. 에이전트가 실행 명령 수행
3. 결과 요약 반환

## 지원 기능

| 기능 | 설명 |
|------|------|
| 에디터 실행 | UnrealEditor.exe 실행 |
| PIE | Play In Editor 모드 |
| 커맨드렛 | UnrealEditor-Cmd.exe -run= |
| 쿠킹 | 콘텐츠 쿠킹 |
| 패키징 | UAT BuildCookRun |
