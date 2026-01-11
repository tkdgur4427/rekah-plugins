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

빌드 관련 작업을 독립 컨텍스트에서 실행합니다.

## 활성화 키워드

- 빌드, build, 컴파일, compile
- 패키징, packaging
- 에디터 빌드, 게임 빌드, 서버 빌드

## 빌드 실행

사용자가 "빌드해줘", "컴파일해줘" 등을 요청하면:

1. `.uproject` 파일 탐색
2. Engine 루트 확인
3. Build.bat 실행
4. 결과 요약 반환

## 빌드 대상

| target | 설명 | 예시 |
|--------|------|------|
| Editor | 에디터 빌드 | `<ProjectName>Editor` |
| Game | 게임 빌드 | `<ProjectName>` |
| Server | 서버 빌드 | `<ProjectName>Server` |

## 빌드 설정

| config | 설명 |
|--------|------|
| Debug | 디버그 빌드 (최적화 없음) |
| Development | 개발 빌드 (기본값) |
| Shipping | 배포 빌드 (최적화됨) |

상세: [BUILD.md](./BUILD.md)
