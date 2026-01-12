---
name: unreal-code-analysis
description: |
  Unreal Engine C++ 코드 분석 시 clangd LSP를 활용하도록 안내합니다.
  "함수 찾아줘", "정의로 이동", "참조 찾기", "심볼 검색" 등에서 활성화됩니다.

context: fork
agent: unreal-code-analysis-agent
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Unreal Code Analysis

MCP LSP 도구를 사용한 정밀한 C++ 코드 분석을 수행합니다.

## 활성화 키워드

- 함수 찾아줘, 정의로 이동, go to definition
- 참조 찾기, find references
- 심볼 검색, workspace symbol
- 클래스 구조, 상속 관계

## MCP LSP 도구

rekah-unreal MCP 서버가 clangd LSP 기능을 직접 제공합니다.

### 사전 요구사항

1. **clangd 설치 확인**: `clangd --version`
2. **compile_commands.json 존재 확인**: 프로젝트 루트에 있어야 함

### 사용 가능한 LSP 도구

| MCP 도구 | 기능 | 설명 |
|----------|------|------|
| `setup_lsp` | LSP 초기화 | 프로젝트 디렉토리 설정 (필수) |
| `lsp_status` | 상태 확인 | 현재 LSP 설정 및 상태 |
| `goToDefinition` | 정의로 이동 | 심볼 정의 위치 찾기 |
| `findReferences` | 참조 찾기 | 모든 참조 위치 검색 |
| `hover` | 호버 정보 | 타입/문서 정보 표시 |
| `documentSymbol` | 문서 심볼 | 파일 내 심볼 목록 |
| `workspaceSymbol` | 워크스페이스 심볼 | 프로젝트 전체 심볼 검색 |
| `goToImplementation` | 구현체 찾기 | 인터페이스 구현체 검색 |
| `incomingCalls` | 호출자 찾기 | 이 함수를 호출하는 함수들 |
| `outgoingCalls` | 피호출자 찾기 | 이 함수가 호출하는 함수들 |

### 사용 예시

```
1. setup_lsp(project_dir="D:/BttUnrealEngine")  # 필수 초기화
2. workspaceSymbol(query="AActor")               # 심볼 검색
3. goToDefinition(file_path="...", line=30, character=10)  # 정의 찾기
```

## compile_commands.json 생성

`compile_commands.json`이 없는 경우 UnrealBuildTool로 생성:

```powershell
# PowerShell
dotnet Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll `
  -mode=GenerateClangDatabase `
  -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" `
  PracticeGame0Editor Win64 Development
```

## LSP 활용

상세: [LSP_USAGE.md](./LSP_USAGE.md)

## 분석 전략

| 분석 유형 | 권장 방법 |
|-----------|-----------|
| 함수/클래스 정의 찾기 | MCP LSP (goToDefinition) |
| 함수 호출 위치 | MCP LSP (findReferences) |
| 심볼 검색 | MCP LSP (workspaceSymbol) |
| 호출 계층 분석 | MCP LSP (incomingCalls/outgoingCalls) |
| 단순 문자열 검색 | grep/Glob |
| 파일명 패턴 검색 | Glob |
