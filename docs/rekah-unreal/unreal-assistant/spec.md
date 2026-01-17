# Unreal Assistant Skill 스펙

> **참고**: 이 문서는 `unreal_utils.py` 기반으로 Claude Code 스킬로 재구현하기 위한 스펙입니다.

## 개요

Unreal Engine 개발 시 반복적으로 수행하는 코드 생성 작업을 자동화하는 스킬입니다.

### 주요 기능

| 기능 | 설명 | 생성 파일 |
|------|------|-----------|
| Class 생성 | UObject/AActor/F류 클래스 생성 | `.h`, `.cpp` |
| Module 생성 | 언리얼 모듈 생성 | `.Build.cs`, `.h`, `.cpp` |
| Plugin 생성 | 언리얼 플러그인 생성 | `.uplugin`, 폴더 구조 |

모든 생성 작업 후에는 `GenerateProjectFiles.bat`을 실행하여 Visual Studio 프로젝트를 업데이트합니다.

---

## 스킬 구조

### 스킬 디렉토리 구조

```
plugins/rekah-unreal/
├── skills/
│   └── unreal-assistant/
│       ├── SKILL.md              # 스킬 정의
│       └── templates/            # 코드 템플릿
│           ├── class/
│           │   ├── raw.h.tmpl
│           │   ├── raw.cpp.tmpl
│           │   ├── uobject.h.tmpl
│           │   ├── uobject.cpp.tmpl
│           │   ├── actor.h.tmpl
│           │   └── actor.cpp.tmpl
│           ├── module/
│           │   ├── Build.cs.tmpl
│           │   ├── Module.h.tmpl
│           │   └── Module.cpp.tmpl
│           └── plugin/
│               └── uplugin.json.tmpl
└── agents/
    └── unreal-assistant-agent.md
```

---

## 클래스 타입 정의

### 1. Raw (F류) - Non-UObject

| 항목 | 값 |
|------|-----|
| Prefix | `F` |
| 부모 클래스 | 없음 |
| UHT 필요 | 아니오 |
| generated.h | 아니오 |

### 2. UObject (U류)

| 항목 | 값 |
|------|-----|
| Prefix | `U` |
| 부모 클래스 | `UObject` |
| UHT 필요 | 예 |
| generated.h | 예 |
| UCLASS 매크로 | 예 |

### 3. Actor (A류)

| 항목 | 값 |
|------|-----|
| Prefix | `A` |
| 부모 클래스 | `AActor` |
| UHT 필요 | 예 |
| generated.h | 예 |
| UCLASS 매크로 | 예 |

---

## 코드 템플릿

### Raw Class (F류)

**Header (`.h`)**
```cpp
#pragma once

#include "CoreMinimal.h"

class F${ClassName}
{
public:
};
```

**Source (`.cpp`)**
```cpp
#include "${ClassName}.h"

/////////////////////////////////////////////////////
// F${ClassName}
```

### UObject Class (U류)

**Header (`.h`)**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "UObject/UObject.h"
#include "${ClassName}.generated.h"

UCLASS(MinimalAPI)
class U${ClassName} : public UObject
{
	GENERATED_UCLASS_BODY()
};
```

**Source (`.cpp`)**
```cpp
#include "${ClassName}.h"

//////////////////////////////////////////////////////////////////////////
// U${ClassName}

U${ClassName}::U${ClassName}(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}
```

### Actor Class (A류)

**Header (`.h`)**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "UObject/ObjectMacros.h"
#include "GameFramework/Actor.h"

#include "${ClassName}.generated.h"

UCLASS()
class A${ClassName} : public AActor
{
	GENERATED_UCLASS_BODY()
};
```

**Source (`.cpp`)**
```cpp
#include "${ClassName}.h"

//////////////////////////////////////////////////////////////////////////
// A${ClassName}

A${ClassName}::A${ClassName}(const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{
}
```

### Module 템플릿

**Build.cs**
```csharp
using UnrealBuildTool;

public class ${ModuleName} : ModuleRules
{
    public ${ModuleName}(ReadOnlyTargetRules Target) : base(Target)
    {
        PublicDependencyModuleNames.AddRange(
			new string[]
            {
                "Core",
                "CoreUObject"
            });

        PrivateDependencyModuleNames.AddRange(
            new string[]
            {

            });

        PublicIncludePaths.AddRange(
			new string[]
            {

            });

        PrivateIncludePaths.AddRange(
            new string[]
            {

            });
    }
}
```

**Module Header (`.h`)**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class F${ModuleName}Module : public FDefaultModuleImpl
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
```

**Module Source (`.cpp`)**
```cpp
#include "${ModuleName}.h"

IMPLEMENT_MODULE(F${ModuleName}Module, ${ModuleName});

void F${ModuleName}Module::StartupModule()
{
	UE_LOG(LogTemp, Log, TEXT("F${ModuleName}Module: Started"));
}

void F${ModuleName}Module::ShutdownModule()
{
	UE_LOG(LogTemp, Log, TEXT("F${ModuleName}Module: Shutdown"));
}
```

### Plugin 템플릿

**.uplugin**
```json
{
  "FileVersion": 3,
  "Version": 1,
  "VersionName": "1.0",
  "FriendlyName": "${PluginName}",
  "Category": "",
  "EnabledByDefault": false,
  "CanContainContent": true
}
```

**폴더 구조**
```
${PluginName}/
├── ${PluginName}.uplugin
├── Source/
├── Content/
└── Config/
```

---

## GenerateProjectFiles 실행

모든 코드 생성 작업 후에는 Visual Studio 프로젝트 파일을 업데이트해야 합니다.

### 실행 방법

```powershell
# Engine 루트의 GenerateProjectFiles.bat 실행
& "<EngineRoot>\Engine\Build\BatchFiles\GenerateProjectFiles.bat" `
    -ProjectFile `
    -Game `
    -Engine `
    -<VSVersion> `
    "<ProjectPath>.uproject"
```

### 파라미터

| 파라미터 | 설명 | 예시 |
|----------|------|------|
| `-ProjectFile` | 프로젝트 파일 생성 | 필수 |
| `-Game` | 게임 프로젝트 포함 | 필수 |
| `-Engine` | 엔진 프로젝트 포함 | 필수 |
| `-<VSVersion>` | Visual Studio 버전 | `-2022` |
| `<ProjectPath>` | .uproject 파일 경로 | 절대 경로 |

### 예시

```powershell
& "D:\BttUnrealEngine\Engine\Build\BatchFiles\GenerateProjectFiles.bat" `
    -ProjectFile `
    -Game `
    -Engine `
    -2022 `
    "D:\BttUnrealEngine\Games\PracticeGame0\PracticeGame0.uproject"
```

---

## SKILL.md 정의

```yaml
---
name: unreal-assistant
description: |
  Unreal Engine 클래스/모듈/플러그인 생성을 지원합니다.
  "클래스 생성", "모듈 추가", "플러그인 생성" 등의 키워드에서 활성화됩니다.
context: fork
agent: unreal-assistant-agent
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Unreal Assistant Skill

코드 생성 작업을 `unreal-assistant-agent`에 위임합니다.

## 활성화 키워드

- 클래스 생성, class 생성, add class
- UObject 생성, Actor 생성
- 모듈 생성, module 생성, add module
- 플러그인 생성, plugin 생성

## 기능

### 1. 클래스 생성

| 타입 | 설명 | Prefix |
|------|------|--------|
| Raw | Non-UObject 클래스 (F류) | `F` |
| UObject | UObject 파생 클래스 | `U` |
| Actor | AActor 파생 클래스 | `A` |

### 2. 모듈 생성

새 모듈 생성 시 다음 파일들이 생성됩니다:
- `<ModuleName>.Build.cs`
- `Public/<ModuleName>.h`
- `Public/<ModuleName>.cpp`

### 3. 플러그인 생성

새 플러그인 생성 시 다음 구조가 생성됩니다:
- `<PluginName>.uplugin`
- `Source/`, `Content/`, `Config/` 폴더

## 동작 순서

1. 사용자 요청 분석 (클래스/모듈/플러그인)
2. 필요한 정보 확인 (이름, 경로, 타입)
3. 템플릿 기반 파일 생성
4. GenerateProjectFiles.bat 실행
5. 결과 반환
```

---

## Agent 정의

```yaml
---
name: unreal-assistant-agent
description: Unreal Engine 코드 생성 전용 경량 에이전트
model: haiku
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# Unreal Assistant Agent

클래스, 모듈, 플러그인 생성을 처리하는 경량 에이전트입니다.

## 역할

1. 사용자 요청 분석
2. 프로젝트 환경 확인 (.uproject, Engine 경로)
3. 템플릿 기반 파일 생성
4. GenerateProjectFiles.bat 실행
5. 결과 요약

## 제한사항

- 기존 코드 수정 금지 (새 파일 생성만)
- 템플릿 외 커스텀 코드 생성 최소화

## 환경 확인

### .uproject 찾기
```powershell
Get-ChildItem -Path . -Filter '*.uproject' -Recurse | Select-Object -First 1
```

### Engine 루트 확인
```powershell
# Engine\Build\BatchFiles\GenerateProjectFiles.bat 존재 확인
Test-Path "<EngineRoot>\Engine\Build\BatchFiles\GenerateProjectFiles.bat"
```

## 대화형 질문 규칙

사용자가 필요한 정보를 명시하지 않은 경우, **한 번에 모든 누락 정보를 질문**합니다.

### 원칙

1. **일괄 질문**: 하나씩 묻지 않고 누락된 정보를 한꺼번에 질문
2. **확답 유도**: 사용자가 한 번에 답변할 수 있도록 형식 제시
3. **기존 정보 활용**: 사용자가 이미 제공한 정보는 다시 묻지 않음

### 질문 형식 예시

**클래스 생성 시:**
```
생성할 경로를 알려주세요:
예: Plugins/BttCore/Source/BttRuntime/Public
예: Engine/Source/Runtime/Core/Public
```

**모듈 생성 시:**
```
모듈을 추가할 플러그인 경로를 알려주세요:
예: Plugins/BttCore
예: Engine/Plugins/MyEnginePlugin
```

**플러그인 생성 시:**
```
플러그인을 생성할 경로를 알려주세요:
예: Plugins (게임 플러그인)
예: Engine/Plugins (엔진 플러그인)
예: Plugins/GameFeatures (GameFeature)
```

---

## 클래스 생성 워크플로우

### 필요 정보

| 항목 | 설명 | 예시 |
|------|------|------|
| 클래스 타입 | Raw/UObject/Actor | Actor |
| 클래스 이름 | Prefix 없이 | MyGameManager |
| 생성 경로 | 최종 경로 (Public/Private 포함) | `Plugins/BttCore/Source/BttRuntime/Public` |

### 워크플로우

1. 사용자 요청에서 정보 추출
2. **경로가 누락되면 질문**
3. 경로 검증 (존재하는 디렉토리인지)
4. 템플릿으로 .h/.cpp 생성
5. GenerateProjectFiles.bat 실행
6. 결과 반환

## 모듈 생성 워크플로우

### 필요 정보

| 항목 | 설명 | 예시 |
|------|------|------|
| 모듈 이름 | 새 모듈 이름 | MyNewModule |
| 플러그인 경로 | 모듈을 추가할 플러그인 | `Plugins/BttCore` |

### 워크플로우

1. 사용자 요청에서 정보 추출
2. **플러그인 경로가 누락되면 질문**
3. 경로 검증 (.uplugin 파일 존재 확인)
4. 디렉토리 구조 생성 (`Source/<ModuleName>/`)
5. .Build.cs, .h, .cpp 생성
6. GenerateProjectFiles.bat 실행
7. 결과 반환

## 플러그인 생성 워크플로우

### 필요 정보

| 항목 | 설명 | 예시 |
|------|------|------|
| 플러그인 이름 | 새 플러그인 이름 | MyAwesomePlugin |
| 생성 경로 | 플러그인을 생성할 위치 | `Plugins`, `Engine/Plugins`, `Plugins/GameFeatures` |

### 워크플로우

1. 사용자 요청에서 정보 추출
2. **생성 경로가 누락되면 질문**
3. 경로 검증 (유효한 디렉토리인지)
4. 디렉토리 구조 생성 (Source, Content, Config)
5. .uplugin 생성
6. GenerateProjectFiles.bat 실행
7. 결과 반환
```

---

## 사용 예시

### 클래스 생성 - 경로 누락 시

```
사용자: MyGameManager 액터 클래스 생성해줘

에이전트: 생성할 경로를 알려주세요:
예: Plugins/BttCore/Source/BttRuntime/Public
예: Engine/Source/Runtime/Core/Public

사용자: Plugins/BttCore/Source/BttRuntime/Public

에이전트:
✓ 클래스 생성 완료
- 타입: Actor (A류)
- 파일: Plugins/BttCore/Source/BttRuntime/Public/MyGameManager.h
- 파일: Plugins/BttCore/Source/BttRuntime/Public/MyGameManager.cpp
- GenerateProjectFiles.bat 실행 완료
```

### 클래스 생성 - 경로 포함 시

```
사용자: Engine/Source/Runtime/Core/Public에 MyHelper F류 클래스 생성해줘

에이전트:
✓ 클래스 생성 완료
- 타입: Raw (F류)
- 파일: Engine/Source/Runtime/Core/Public/MyHelper.h
- 파일: Engine/Source/Runtime/Core/Public/MyHelper.cpp
- GenerateProjectFiles.bat 실행 완료
```

### 모듈 생성

```
사용자: MyNewModule 모듈 추가해줘

에이전트: 모듈을 추가할 플러그인 경로를 알려주세요:
예: Plugins/BttCore
예: Engine/Plugins/MyEnginePlugin

사용자: Plugins/BttCore

에이전트:
✓ 모듈 생성 완료
- 경로: Plugins/BttCore/Source/MyNewModule/
- 파일: MyNewModule.Build.cs
- 파일: Public/MyNewModule.h
- 파일: Public/MyNewModule.cpp
- GenerateProjectFiles.bat 실행 완료
```

### 플러그인 생성 - 경로 누락 시

```
사용자: MyAwesomePlugin 플러그인 만들어줘

에이전트: 플러그인을 생성할 경로를 알려주세요:
예: Plugins (게임 플러그인)
예: Engine/Plugins (엔진 플러그인)
예: Plugins/GameFeatures (GameFeature)

사용자: Plugins/GameFeatures

에이전트:
✓ 플러그인 생성 완료
- 경로: Plugins/GameFeatures/MyAwesomePlugin/
- 파일: MyAwesomePlugin.uplugin
- 폴더: Source/, Content/, Config/
- GenerateProjectFiles.bat 실행 완료
```

### 플러그인 생성 - 경로 포함 시

```
사용자: Engine/Plugins에 MyEnginePlugin 플러그인 만들어줘

에이전트:
✓ 플러그인 생성 완료
- 경로: Engine/Plugins/MyEnginePlugin/
- 파일: MyEnginePlugin.uplugin
- 폴더: Source/, Content/, Config/
- GenerateProjectFiles.bat 실행 완료
```

---

## 고려사항

### 1. 경로 기반 질문

- 클래스: **최종 경로** 한 번에 질문 (플러그인/모듈/Public 따로 묻지 않음)
- 모듈: **플러그인 경로**만 질문
- 플러그인: **생성 위치**만 질문
- 경로를 이미 제공했으면 질문 없이 바로 진행

### 2. 경로 검증

- 클래스 생성: 지정 경로가 존재하는지 확인
- 모듈 생성: .uplugin 파일이 있는 플러그인인지 확인
- 플러그인 생성: 유효한 디렉토리인지 확인 (존재 여부)
- 검증 실패 시 에러 메시지와 함께 재질문

### 3. 지원 위치

| 대상 | 가능한 위치 |
|------|------------|
| 클래스 | 게임 모듈, 플러그인 모듈, 엔진 모듈 |
| 모듈 | 게임 플러그인, 엔진 플러그인 |
| 플러그인 | Plugins, Engine/Plugins, Plugins/GameFeatures |

### 4. 이름 규칙

- 클래스 이름은 Prefix 없이 입력 (MyClass)
- 생성 시 타입에 맞는 Prefix 자동 추가 (FMyClass, UMyClass, AMyClass)

### 5. 기존 파일 덮어쓰기 방지

- 동일한 이름의 파일이 존재하면 경고 후 중단
- 사용자 확인 후 진행 가능

### 6. .uplugin 모듈 등록

- Plugin 생성 시 초기 모듈은 생성하지 않음
- Module 생성 시 .uplugin에 자동 등록 검토 (향후 기능)

---

## 향후 확장

1. **커스텀 부모 클래스 지정**: AActor 대신 ACharacter 등 지정 가능
2. **인터페이스 생성**: UInterface 기반 인터페이스 클래스
3. **Component 생성**: UActorComponent, USceneComponent 등
4. **.uplugin 모듈 자동 등록**: 모듈 생성 시 플러그인에 자동 등록
5. **Editor Module 지원**: Editor 전용 모듈 템플릿
