---
name: build
description: Unreal 프로젝트 빌드 실행
---

# Build Command

rekah-unreal MCP 서버의 `build_unreal_project` tool을 사용하여 프로젝트를 빌드합니다.

## 사용법

```
/rekah-unreal:build [target] [config]
```

## 파라미터

| 파라미터 | 설명 | 기본값 | 옵션 |
|----------|------|--------|------|
| target | 빌드 타겟 | Editor | Editor, Game, Server |
| config | 빌드 설정 | Development | Debug, Development, Shipping |

## 예시

```
# 에디터 빌드 (Development)
/rekah-unreal:build

# 게임 빌드 (Shipping)
/rekah-unreal:build Game Shipping

# 서버 빌드 (Development)
/rekah-unreal:build Server
```

## 동작

1. 현재 프로젝트의 `.uproject` 파일 탐색
2. Unreal Engine 루트 디렉토리 탐색
3. `Engine/Build/BatchFiles/Build.bat` 실행
4. 빌드 결과 반환
