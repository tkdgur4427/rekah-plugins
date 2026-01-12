---
name: unreal-code-analysis
description: |
  Unreal Engine C++ 코드 분석을 지원합니다.
  "함수 찾아줘", "정의로 이동", "참조 찾기", "심볼 검색" 등의 키워드에서 활성화됩니다.
context: fork
agent: unreal-code-analysis-agent
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Unreal Code Analysis Skill

코드 분석 작업을 `unreal-code-analysis-agent`에 위임합니다.

## 활성화 키워드

- 함수 찾아줘, 정의로 이동, go to definition
- 참조 찾기, find references
- 심볼 검색, workspace symbol
- 호출 계층, incoming calls, outgoing calls
- 클래스 구조, 상속 관계, 구현체 찾기

## 동작

1. 스킬 활성화 시 `unreal-code-analysis-agent` 호출
2. 에이전트가 MCP LSP 도구로 코드 분석 수행
3. 결과 요약 반환

## MCP LSP 도구

| 도구 | 기능 |
|------|------|
| `setup_lsp` | LSP 초기화 (필수) |
| `goToDefinition` | 정의로 이동 |
| `findReferences` | 참조 찾기 |
| `hover` | 타입/문서 정보 |
| `workspaceSymbol` | 심볼 검색 |
| `goToImplementation` | 구현체 찾기 |
| `incomingCalls` | 호출자 찾기 |
| `outgoingCalls` | 피호출자 찾기 |

## 사전 요구사항

1. **clangd 설치**: `clangd --version`
2. **compile_commands.json**: 프로젝트 루트에 존재

상세 사용법은 에이전트 문서 참조.
