# Unreal Engine 커맨드렛 가이드

## 커맨드렛 실행 형식

```
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "<ProjectPath>" -run=<CommandletName> [Options]
```

## 자주 사용하는 커맨드렛

| 커맨드렛 | 용도 | 예시 옵션 |
|----------|------|-----------|
| `Resave` | 패키지 재저장 | `-Package=/Game/Maps/MainMenu` |
| `Fixup` | 에셋 수정 | |
| `DumpBlueprintBytecode` | BP 바이트코드 덤프 | `-Blueprint=/Game/BP/MyBP` |
| `TextAsset` | 텍스트 에셋 처리 | |
| `AssetRegister` | 에셋 레지스트리 생성 | |
| `CompileAllBlueprintAssets` | 모든 BP 컴파일 | |

## 예시

### Resave 커맨드렛

```bash
# 특정 패키지 재저장
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -run=Resave -Package=/Game/Maps/MainMenu

# 모든 맵 재저장
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -run=Resave -Package=/Game/Maps/
```

### 블루프린트 컴파일

```bash
# 모든 블루프린트 컴파일
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -run=CompileAllBlueprintAssets
```

### 에셋 레지스트리 생성

```bash
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -run=AssetRegister
```

## 쿠킹

### 기본 쿠킹 명령

```bash
Engine\Binaries\Win64\UnrealEditor-Cmd.exe "D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" -run=Cook -TargetPlatform=WindowsNoEditor
```

### 플랫폼별 쿠킹

| 플랫폼 | TargetPlatform |
|--------|----------------|
| Windows | `WindowsNoEditor` |
| Linux | `LinuxNoEditor` |
| Mac | `MacNoEditor` |
| Android | `Android` |
| iOS | `IOS` |

## 패키징 (UAT 사용)

### 기본 패키징

```bash
Engine\Build\BatchFiles\RunUAT.bat BuildCookRun ^
  -project="D:/BttUnrealEngine/Games/PracticeGame0/PracticeGame0.uproject" ^
  -platform=Win64 ^
  -configuration=Shipping ^
  -cook ^
  -stage ^
  -pak ^
  -archive
```

### UAT 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-cook` | 콘텐츠 쿠킹 |
| `-stage` | 스테이징 |
| `-pak` | PAK 파일 생성 |
| `-archive` | 아카이브 생성 |
| `-compressed` | 압축 활성화 |
| `-clean` | 클린 빌드 |

## 실행 순서

### 1. 프로젝트 탐색

```bash
find . -maxdepth 3 -name "*.uproject" 2>/dev/null | head -1
```

### 2. 커맨드렛 실행

사용자가 요청한 커맨드렛에 맞는 명령 구성 후 실행.

### 3. 결과 반환

- **성공 시**: "커맨드렛 실행 완료."
- **실패 시**: "커맨드렛 실행 실패. 에러: [에러 메시지]"

## 유용한 옵션

| 옵션 | 설명 |
|------|------|
| `-NoLogTimes` | 로그에 타임스탬프 제거 |
| `-Verbose` | 상세 로그 출력 |
| `-Unattended` | 무인 모드 (프롬프트 없음) |
| `-AllowStdOutLogVerbosity` | stdout에 로그 출력 |
