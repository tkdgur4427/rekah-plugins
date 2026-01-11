---
name: say-hello
description: MCP 연결 테스트용 간단한 인사 커맨드
---

# Say Hello Command

rekah-unreal MCP 서버의 `say_hello` tool을 사용하여 MCP 연결을 테스트합니다.

> **목적**: 이 커맨드는 MCP 연결 테스트용 임시 커맨드입니다.

## 사용법

```
/rekah-unreal:say-hello [name]
```

## 파라미터

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| name | 인사할 이름 | World |

## 예시

```
# 기본 인사
/rekah-unreal:say-hello

# 이름 지정
/rekah-unreal:say-hello Claude
```

## 동작

1. MCP 서버의 `say_hello` 도구 호출
2. 인사 메시지 반환

## 예상 결과

```
Hello, World! MCP connection is working correctly.
```

또는

```
Hello, Claude! MCP connection is working correctly.
```
