---
name: unreal-assistant
description: |
  Unreal Engine 클래스/모듈/플러그인 생성을 지원합니다.
  "클래스 생성", "모듈 추가", "플러그인 생성" 등의 키워드에서 활성화됩니다.
context: fork
agent: unreal-assistant-agent
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Unreal Assistant Skill

코드 생성 작업을 `unreal-assistant-agent`에 위임합니다.

## 활성화 키워드

- 클래스 생성, class 생성, add class
- UObject 생성, Actor 생성
- 모듈 생성, module 생성, add module
- 플러그인 생성, plugin 생성

## 기능

### 1. 클래스 생성

| 타입 | 설명 | Prefix |
|------|------|--------|
| Raw | Non-UObject 클래스 (F류) | `F` |
| UObject | UObject 파생 클래스 | `U` |
| Actor | AActor 파생 클래스 | `A` |

### 2. 모듈 생성

새 모듈 생성 시 다음 파일들이 생성됩니다:
- `<ModuleName>.Build.cs`
- `Public/<ModuleName>.h`
- `Public/<ModuleName>.cpp`

### 3. 플러그인 생성

새 플러그인 생성 시 다음 구조가 생성됩니다:
- `<PluginName>.uplugin`
- `Source/`, `Content/`, `Config/` 폴더

## 동작 순서

1. 사용자 요청 분석 (클래스/모듈/플러그인)
2. 필요한 정보 확인 (이름, 경로, 타입)
3. 템플릿 기반 파일 생성
4. GenerateProjectFiles.bat 실행
5. 결과 반환
