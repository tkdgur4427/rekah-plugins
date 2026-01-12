# MCP LSP 도구 사용 가이드

## 개요

rekah-unreal MCP 서버가 clangd LSP 기능을 직접 제공합니다.
Claude Code의 내장 LSP Tool 버그를 우회하여 정확한 C++ 코드 분석이 가능합니다.

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

## MCP LSP 도구

### 초기화 (필수)

LSP 기능을 사용하기 전에 반드시 `setup_lsp`를 호출해야 합니다:

```
setup_lsp(project_dir="D:/BttUnrealEngine")
```

**반환:**
```
✅ LSP initialized successfully!
  Project: D:/BttUnrealEngine
  compile_commands.json: D:\BttUnrealEngine\compile_commands.json

You can now use LSP tools:
  - goToDefinition, findReferences, hover
  - documentSymbol, workspaceSymbol, goToImplementation
  - prepareCallHierarchy, incomingCalls, outgoingCalls
```

### 상태 확인

```
lsp_status()
```

**반환:**
```
📊 LSP Status: INITIALIZED
  Project: D:\BttUnrealEngine
  clangd running: Yes
  Open files: 1
```

---

## P0: 핵심 도구

### 1. goToDefinition - 정의로 이동

심볼의 정의 위치를 찾습니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)

**예시:**
```
goToDefinition(
    file_path="D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h",
    line=30,
    character=10
)
```

**반환:**
```
Definition location(s):
  D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h:256:7
```

### 2. findReferences - 참조 찾기

심볼이 사용되는 모든 위치를 찾습니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)
- `include_declaration`: 선언부 포함 여부 (기본값: true)

**예시:**
```
findReferences(
    file_path="D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h",
    line=256,
    character=10,
    include_declaration=true
)
```

### 3. hover - 호버 정보

심볼의 타입과 문서화 정보를 가져옵니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)

**예시:**
```
hover(
    file_path="D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h",
    line=30,
    character=10
)
```

**반환:**
```
Hover information:
class AActor

Size: 1136 bytes
Actor is the base class for an Object that can be placed or spawned in a level.
...
```

---

## P1: 확장 도구

### 4. documentSymbol - 문서 심볼

파일 내 모든 심볼(클래스, 함수, 변수 등)을 가져옵니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로

**예시:**
```
documentSymbol(file_path="D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h")
```

**반환:**
```
Symbols in Actor.h:
Class: AActor (line 30)
Class: AController (line 31)
...
```

### 5. workspaceSymbol - 워크스페이스 심볼

프로젝트 전체에서 심볼을 검색합니다.

**파라미터:**
- `query`: 검색할 심볼 이름 (부분 일치 지원)

**예시:**
```
workspaceSymbol(query="AActor")
workspaceSymbol(query="BeginPlay")
workspaceSymbol(query="GetComponents")
```

### 6. goToImplementation - 구현체 찾기

인터페이스나 추상 메서드의 구현체를 찾습니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)

---

## P2: 호출 계층 도구

### 7. incomingCalls - 호출자 찾기

특정 함수를 호출하는 모든 함수를 찾습니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)

**예시:**
```
incomingCalls(
    file_path="D:/BttUnrealEngine/Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h",
    line=2128,
    character=10
)
```

### 8. outgoingCalls - 피호출자 찾기

특정 함수가 호출하는 모든 함수를 찾습니다.

**파라미터:**
- `file_path`: 소스 파일 절대 경로
- `line`: 라인 번호 (1-based)
- `character`: 컬럼 번호 (1-based)

---

## grep vs MCP LSP 선택 기준

| 상황 | 권장 방식 | 이유 |
|------|-----------|------|
| 특정 클래스/함수 정의 찾기 | **MCP LSP** | 정확한 심볼 매칭 |
| 함수가 호출되는 모든 위치 | **MCP LSP** | 컨텍스트 인식 |
| 상속/구현 관계 파악 | **MCP LSP** | 타입 시스템 이해 |
| 호출 계층 분석 | **MCP LSP** | 정확한 호출 그래프 |
| 단순 문자열 패턴 검색 | grep | 빠른 검색 |
| 주석/문서 내용 검색 | grep | LSP는 코드만 분석 |
| 파일명 패턴으로 찾기 | Glob | 파일 시스템 검색 |

## 성능 고려사항

### 대규모 프로젝트에서

Unreal Engine처럼 대규모 프로젝트에서는:

1. **초기 인덱싱 시간**: 첫 파일 열 때 인덱싱에 시간 소요 (0.3~1초)
2. **후속 응답**: 인덱싱 후 즉시 응답
3. **메모리 사용량**: clangd가 백그라운드에서 실행됨

### 정확도

| 방식 | 정확도 |
|------|--------|
| MCP LSP | ~99% |
| grep 패턴 | ~70% |

## 문제 해결

### LSP 초기화 안 됨

```
⚠️ LSP not initialized!
Please call 'setup_lsp' tool first with your Unreal Engine project directory.
Example: setup_lsp(project_dir="D:/MyUnrealProject")
```

**해결:** `setup_lsp` 호출

### compile_commands.json 없음

**해결:** UnrealBuildTool로 생성 (위 섹션 참조)

### clangd 없음

**해결:** LLVM 설치 (`choco install llvm` 또는 `winget install LLVM.LLVM`)

### 심볼 못 찾음

1. `compile_commands.json` 재생성
2. 새 세션 시작 (MCP 서버 재시작)
3. `setup_lsp` 다시 호출
