# Unreal Editor 실행 가이드

## 에디터 실행 명령

### 기본 형식

```
Engine\Binaries\Win64\UnrealEditor.exe "<ProjectPath>" [Options]
```

### 예시

```bash
# 기본 에디터 실행
Engine\Binaries\Win64\UnrealEditor.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject"

# 특정 맵과 함께 실행
Engine\Binaries\Win64\UnrealEditor.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" /Game/Maps/MainMenu
```

## 실행 옵션

| 옵션 | 설명 |
|------|------|
| `/Game/Path/To/Map` | 특정 맵 열기 |
| `-game` | 게임 모드로 실행 (PIE) |
| `-server` | 서버 모드로 실행 |
| `-log` | 로그 창 표시 |
| `-debug` | 디버그 모드 |
| `-nosplash` | 스플래시 화면 건너뛰기 |

## PIE (Play In Editor) 실행

```bash
# PIE 모드로 실행
Engine\Binaries\Win64\UnrealEditor.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -game

# 특정 맵에서 PIE 실행
Engine\Binaries\Win64\UnrealEditor.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" /Game/Maps/MainMenu -game
```

## 실행 순서

### 1. 프로젝트 탐색

```bash
# .uproject 파일 찾기
find . -maxdepth 3 -name "*.uproject" 2>/dev/null | head -1
```

### 2. 에디터 경로 확인

```bash
# 에디터 바이너리 확인
ls Engine/Binaries/Win64/UnrealEditor.exe
```

### 3. 에디터 실행

```bash
# 백그라운드로 실행 (터미널 블로킹 방지)
start "" "Engine\Binaries\Win64\UnrealEditor.exe" "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject"
```

## 결과 처리

- **성공 시**: "에디터가 실행되었습니다."
- **실패 시**: "에디터 실행 실패. 에러: [에러 메시지]"

> **참고**: 에디터는 백그라운드에서 실행되므로, 터미널이 블로킹되지 않습니다.
