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

LSP 기반 코드 분석을 독립 컨텍스트에서 실행합니다.

## 활성화 키워드

- 함수 찾아줘, 정의로 이동, go to definition
- 참조 찾기, find references
- 심볼 검색, workspace symbol
- 클래스 구조, 상속 관계

## 사전 체크

1. **clangd 설치 확인**: `clangd --version`
2. **compile_commands.json 존재 확인**: 프로젝트 루트에 있어야 함
3. **.lsp.json 존재 확인**: LSP 설정 파일

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
| 함수/클래스 정의 찾기 | LSP (go to definition) |
| 함수 호출 위치 | LSP (find references) |
| 심볼 검색 | LSP (workspace symbol) |
| 단순 문자열 검색 | grep/Glob |
| 파일명 패턴 검색 | Glob |
