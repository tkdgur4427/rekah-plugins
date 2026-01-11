# Unreal Engine 빌드 가이드

## 빌드 명령 형식

```
Engine\Build\BatchFiles\Build.bat <TargetName> <Platform> <Config> -project="<ProjectPath>" -WaitMutex
```

## 인자 설명

| 인자 | 설명 | 예시 |
|------|------|------|
| TargetName | `<ProjectName>` + target suffix | `PracticeGame0Editor`, `PracticeGame0`, `PracticeGame0Server` |
| Platform | 플랫폼 | `Win64`, `Linux`, `Mac` |
| Config | 빌드 설정 | `Debug`, `Development`, `Shipping` |
| -project | .uproject 경로 | 절대 경로 권장 |
| -WaitMutex | 병렬 빌드 충돌 방지 | 항상 포함 권장 |

## 타겟 이름 규칙

| target 파라미터 | TargetName 생성 규칙 | 예시 |
|-----------------|---------------------|------|
| Editor | `<ProjectName>Editor` | PracticeGame0Editor |
| Game | `<ProjectName>` | PracticeGame0 |
| Server | `<ProjectName>Server` | PracticeGame0Server |

## 빌드 예시

### 에디터 빌드 (Development)

```bash
Engine\Build\BatchFiles\Build.bat PracticeGame0Editor Win64 Development -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -WaitMutex
```

### 게임 빌드 (Shipping)

```bash
Engine\Build\BatchFiles\Build.bat PracticeGame0 Win64 Shipping -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -WaitMutex
```

### 서버 빌드 (Development)

```bash
Engine\Build\BatchFiles\Build.bat PracticeGame0Server Win64 Development -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -WaitMutex
```

## 빌드 실행 순서

### 1. 프로젝트 탐색

```bash
# .uproject 파일 찾기 (Windows)
dir /s /b *.uproject | findstr /r "^.*\.uproject$"

# .uproject 파일 찾기 (bash)
find . -maxdepth 3 -name "*.uproject" 2>/dev/null | head -1

# Engine 루트 확인
ls Engine/Build/BatchFiles/Build.bat
```

### 2. 프로젝트 이름 추출

.uproject 파일명에서 프로젝트 이름을 추출합니다:
- `PracticeGame0.uproject` → `PracticeGame0`

### 3. 빌드 명령 구성

사용자 요청에 따라 TargetName을 구성:
- "에디터 빌드해줘" → `PracticeGame0Editor`
- "게임 빌드해줘" → `PracticeGame0`
- "서버 빌드해줘" → `PracticeGame0Server`

### 4. 빌드 실행

```bash
Engine\Build\BatchFiles\Build.bat <TargetName> Win64 Development -project="<ProjectPath>" -WaitMutex
```

## 빌드 결과 처리

빌드 완료 후 결과를 main session에 요약하여 보고:

- **성공 시**: "빌드가 성공적으로 완료되었습니다. (소요 시간: X분 Y초)"
- **실패 시**: "빌드 실패. 에러: [에러 메시지 요약]"

## 추가 빌드 옵션

| 옵션 | 설명 |
|------|------|
| `-NoUBTMakefiles` | UBT makefile 생성 건너뛰기 |
| `-NoXGE` | XGE 빌드 비활성화 |
| `-Rebuild` | 전체 리빌드 |
| `-Clean` | 빌드 전 클린 |
