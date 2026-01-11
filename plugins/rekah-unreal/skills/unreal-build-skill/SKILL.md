---
name: unreal-build-skill
description: |
  Unreal Engine 프로젝트 빌드를 지원합니다.
  "빌드", "컴파일", "패키징" 등의 키워드에서 활성화됩니다.
context: fork
agent: unreal-build-agent
allowed-tools:
  - Bash
  - Read
  - Glob
---

# Unreal Build Skill

빌드 관련 작업을 `unreal-build-agent`에 위임합니다.

## 활성화 키워드

- 빌드, build, 컴파일, compile
- 패키징, packaging
- 에디터 빌드, 게임 빌드, 서버 빌드

## 동작

1. 스킬 활성화 시 `unreal-build-agent` 호출
2. 에이전트가 빌드 명령 실행
3. 결과 요약 반환

## 빌드 대상

| target | 설명 |
|--------|------|
| Editor | 에디터 빌드 |
| Game | 게임 빌드 |
| Server | 서버 빌드 |

## 빌드 설정

| config | 설명 |
|--------|------|
| Debug | 디버그 빌드 |
| Development | 개발 빌드 (기본값) |
| Shipping | 배포 빌드 |
