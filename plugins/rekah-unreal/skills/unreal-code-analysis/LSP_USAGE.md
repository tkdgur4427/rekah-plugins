# LSP 활용 가이드

## 개요

Unreal Engine C++ 코드 분석 시 grep 대신 clangd LSP를 활용하면 정확한 심볼 탐색이 가능합니다.

## 사전 요구사항

### 1. clangd 설치

```powershell
# 설치 확인
clangd --version

# Windows (Chocolatey)
choco install llvm

# Windows (winget)
winget install LLVM.LLVM
```

### 2. compile_commands.json 생성

UnrealBuildTool을 사용하여 생성:

```powershell
# PowerShell
dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll `
  -mode=GenerateClangDatabase `
  -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" `
  PracticeGame0Editor Win64 Development
```

**인자 설명:**
- `-mode=GenerateClangDatabase`: clangd용 컴파일 데이터베이스 생성 모드
- `-project=`: 프로젝트 파일 경로 (절대 경로 권장)
- `<ProjectName>Editor`: 타겟 이름 (Editor 타겟 권장)
- `Win64`: 플랫폼
- `Development`: 빌드 구성

### 3. .lsp.json 설정

프로젝트 루트에 `.lsp.json` 파일 생성:

```json
{
  "clangd": {
    "command": "clangd",
    "args": [
      "--log=verbose",
      "--pretty",
      "--background-index",
      "--compile-commands-dir=${PROJECT_DIR}",
      "-j=2",
      "--background-index-priority=background"
    ],
    "extensionToLanguage": {
      ".cpp": "cpp",
      ".cc": "cpp",
      ".h": "cpp",
      ".hpp": "cpp",
      ".inl": "cpp"
    },
    "startupTimeout": 10000,
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

## LSP 명령

### 1. 정의로 이동 (Go to Definition)

특정 심볼의 정의를 찾을 때 사용합니다.

**용도:**
- 함수 구현부 찾기
- 클래스 정의 찾기
- 변수 선언 위치 찾기

**예시:**
```
GetComponents() 함수의 정의를 찾아줘
→ LSP의 "go to definition" 사용
```

### 2. 참조 찾기 (Find References)

특정 심볼이 사용되는 모든 위치를 찾습니다.

**용도:**
- 함수 호출 위치 찾기
- 변수 사용 위치 찾기
- 리팩토링 영향 범위 파악

**예시:**
```
GetComponents() 함수가 어디서 호출되는지 찾아줘
→ LSP의 "find references" 사용
```

### 3. 심볼 검색 (Workspace Symbol)

프로젝트 전체에서 심볼을 검색합니다.

**용도:**
- 클래스/함수명으로 검색
- 부분 일치 검색
- 프로젝트 전체 탐색

**예시:**
```
Actor로 시작하는 클래스들을 찾아줘
→ LSP의 "workspace symbol" 사용
```

## grep vs LSP 선택 기준

| 상황 | 권장 방식 | 이유 |
|------|-----------|------|
| 특정 클래스/함수 정의 찾기 | **LSP** | 정확한 심볼 매칭 |
| 함수가 호출되는 모든 위치 | **LSP** | 컨텍스트 인식 |
| 상속/구현 관계 파악 | **LSP** | 타입 시스템 이해 |
| 단순 문자열 패턴 검색 | grep | 빠른 검색 |
| 주석/문서 내용 검색 | grep | LSP는 코드만 분석 |
| 파일명 패턴으로 찾기 | Glob | 파일 시스템 검색 |

## 성능 고려사항

### 대규모 프로젝트에서

Unreal Engine처럼 대규모 프로젝트에서는:

1. **초기 인덱싱 시간**: 첫 실행 시 인덱싱에 시간 소요
2. **백그라운드 인덱싱**: `--background-index` 옵션으로 점진적 인덱싱
3. **메모리 사용량**: 대규모 프로젝트에서는 메모리 사용량 증가

### 최적화 팁

```json
{
  "clangd": {
    "args": [
      "-j=2",                              // 병렬 작업 제한
      "--background-index-priority=background",  // 백그라운드 우선순위
      "--pch-storage=memory",             // PCH 메모리 저장
      "--limit-results=100"               // 결과 수 제한
    ]
  }
}
```

## 문제 해결

### compile_commands.json 오류

```powershell
# 파일 존재 확인
Test-Path compile_commands.json

# 파일 크기 확인
(Get-Item compile_commands.json).Length / 1MB
```

### clangd 연결 실패

```powershell
# clangd 버전 확인
clangd --version

# clangd 직접 실행 테스트
clangd --check=Engine/Source/Runtime/Engine/Public/Engine.h
```

### 심볼 못 찾음

1. `compile_commands.json` 재생성
2. clangd 재시작
3. 인덱싱 완료 대기
