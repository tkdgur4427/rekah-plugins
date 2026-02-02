# Unreal Assistant Skill 구현 계획

> **스펙 참조**: [spec.md](./spec.md)

## 개요

`unreal_utils.py` 기반의 Unreal Engine 코드 생성 기능을 Claude Code 스킬로 구현합니다.

---

## 구현 대상 파일

### 1. SKILL.md
```
plugins/rekah-unreal/skills/unreal-assistant/SKILL.md
```

### 2. Agent 정의
```
plugins/rekah-unreal/agents/unreal-assistant-agent.md
```

### 3. 템플릿 파일
```
plugins/rekah-unreal/skills/unreal-assistant/templates/
├── class/
│   ├── raw.h.tmpl
│   ├── raw.cpp.tmpl
│   ├── uobject.h.tmpl
│   ├── uobject.cpp.tmpl
│   ├── actor.h.tmpl
│   └── actor.cpp.tmpl
├── module/
│   ├── Build.cs.tmpl
│   ├── Module.h.tmpl
│   └── Module.cpp.tmpl
└── plugin/
    └── uplugin.json.tmpl
```

---

## 구현 순서

### Phase 1: 기본 구조 생성

1. **디렉토리 생성**
   - `skills/unreal-assistant/` 폴더
   - `skills/unreal-assistant/templates/` 하위 폴더들

2. **SKILL.md 작성**
   - spec.md의 SKILL.md 정의 섹션 참조
   - 기존 `unreal-build-skill/SKILL.md` 형식 참고

3. **Agent 파일 작성**
   - `agents/unreal-assistant-agent.md`
   - 기존 `unreal-build-agent.md` 형식 참고

### Phase 2: 템플릿 파일 생성

1. **Class 템플릿** (6개 파일)
   - Raw: `raw.h.tmpl`, `raw.cpp.tmpl`
   - UObject: `uobject.h.tmpl`, `uobject.cpp.tmpl`
   - Actor: `actor.h.tmpl`, `actor.cpp.tmpl`

2. **Module 템플릿** (3개 파일)
   - `Build.cs.tmpl`
   - `Module.h.tmpl`
   - `Module.cpp.tmpl`

3. **Plugin 템플릿** (1개 파일)
   - `uplugin.json.tmpl`

### Phase 3: 검증 및 테스트

아래 테스트 계획 섹션 참조

---

## 테스트 계획

### 1. 파일 구조 검증 (자동화 가능)

스킬 구현 후 필수 파일 존재 여부 확인:

```powershell
# 필수 파일 존재 확인
$requiredFiles = @(
    "plugins/rekah-unreal/skills/unreal-assistant/SKILL.md",
    "plugins/rekah-unreal/agents/unreal-assistant-agent.md",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/raw.h.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/raw.cpp.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/uobject.h.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/uobject.cpp.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/actor.h.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/class/actor.cpp.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/module/Build.cs.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/module/Module.h.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/module/Module.cpp.tmpl",
    "plugins/rekah-unreal/skills/unreal-assistant/templates/plugin/uplugin.json.tmpl"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "[OK] $file" -ForegroundColor Green
    } else {
        Write-Host "[MISSING] $file" -ForegroundColor Red
    }
}
```

### 2. SKILL.md 구문 검증

YAML frontmatter 필수 항목 확인:
- `name`: 스킬 이름
- `description`: 설명
- `context`: fork/main
- `agent`: 에이전트 참조
- `allowed-tools`: 허용 도구 목록

```powershell
# SKILL.md frontmatter 검증
$content = Get-Content "plugins/rekah-unreal/skills/unreal-assistant/SKILL.md" -Raw
if ($content -match "^---[\s\S]*?---") {
    Write-Host "[OK] YAML frontmatter found" -ForegroundColor Green
} else {
    Write-Host "[ERROR] YAML frontmatter missing" -ForegroundColor Red
}
```

### 3. 템플릿 변수 검증

각 템플릿에 필요한 변수(`${ClassName}`, `${ModuleName}`, `${PluginName}`)가 올바르게 포함되어 있는지 확인:

```powershell
# Class 템플릿 검증
$classTemplates = Get-ChildItem "plugins/rekah-unreal/skills/unreal-assistant/templates/class/*.tmpl"
foreach ($tmpl in $classTemplates) {
    $content = Get-Content $tmpl -Raw
    if ($content -match '\$\{ClassName\}') {
        Write-Host "[OK] ${ClassName} found in $($tmpl.Name)" -ForegroundColor Green
    } else {
        Write-Host "[WARN] ${ClassName} not found in $($tmpl.Name)" -ForegroundColor Yellow
    }
}
```

### 4. 스킬 로딩 테스트 (수동)

Claude Code에서 스킬이 정상적으로 로드되는지 확인:

```
# Claude Code 세션에서 실행
/skills
```

예상 결과: `unreal-assistant` 스킬이 목록에 표시됨

### 5. 기능 테스트 (수동, Unreal 프로젝트 필요)

Unreal Engine 프로젝트에서 실제 동작 테스트:

#### 5.1 경로 기반 질문 테스트

| 테스트 케이스 | 입력 | 기대 동작 |
|--------------|------|----------|
| 클래스 - 경로 누락 | "MyClass 액터 생성해줘" | **최종 경로**를 한 번에 질문 |
| 클래스 - 경로 포함 | "Plugins/BttCore/Source/BttRuntime/Public에 MyClass 액터" | 질문 없이 바로 생성 |
| 모듈 - 경로 누락 | "MyModule 모듈 추가해줘" | **플러그인 경로**만 질문 |
| 모듈 - 경로 포함 | "Plugins/BttCore에 MyModule 모듈 추가" | 질문 없이 바로 생성 |
| 플러그인 - 경로 누락 | "MyPlugin 플러그인 생성해줘" | **생성 위치**만 질문 |
| 플러그인 - 경로 포함 | "Engine/Plugins에 MyPlugin 플러그인" | 질문 없이 바로 생성 |

#### 5.2 클래스 생성 테스트

| 테스트 케이스 | 입력 | 기대 결과 |
|--------------|------|----------|
| Actor 클래스 | "MyGameManager 액터 클래스 생성해줘" → 질문 응답 | 지정 경로에 `.h`, `.cpp` 생성 |
| UObject 클래스 | "TestObject UObject 생성해줘" → 질문 응답 | 지정 경로에 `.h`, `.cpp` 생성 |
| Raw 클래스 | "HelperClass F류 클래스 생성해줘" → 질문 응답 | 지정 경로에 `.h`, `.cpp` 생성 |

#### 5.3 모듈 생성 테스트

| 테스트 케이스 | 입력 | 기대 결과 |
|--------------|------|----------|
| 새 모듈 | "MyNewModule 모듈 추가해줘" → 플러그인 응답 | 지정 플러그인에 `.Build.cs`, `.h`, `.cpp` 생성 |

#### 5.4 플러그인 생성 테스트

| 테스트 케이스 | 입력 | 기대 결과 |
|--------------|------|----------|
| 새 플러그인 | "MyPlugin 플러그인 만들어줘" | `.uplugin` + 폴더 구조 생성 (질문 없이) |

#### 5.5 GenerateProjectFiles 실행 테스트

모든 생성 작업 후 `GenerateProjectFiles.bat`이 실행되는지 확인:
- 에이전트 출력에서 "GenerateProjectFiles" 실행 메시지 확인
- Visual Studio 솔루션 파일 업데이트 확인

### 6. 에러 케이스 테스트 (수동)

| 테스트 케이스 | 입력 | 기대 동작 |
|--------------|------|----------|
| 중복 파일 | 이미 존재하는 클래스명으로 생성 시도 | 경고 메시지 출력, 덮어쓰기 방지 |
| 클래스 - 잘못된 경로 | 존재하지 않는 경로 지정 | 경로 검증 실패, 재질문 |
| 모듈 - 잘못된 플러그인 | .uplugin 없는 경로 지정 | "플러그인이 아닙니다" 메시지 |
| 플러그인 - 잘못된 위치 | 존재하지 않는 디렉토리 | 경로 검증 실패, 재질문 |
| Engine 경로 오류 | Engine 디렉토리가 없는 환경 | GenerateProjectFiles 실행 불가 메시지 |

### 7. 빌드 검증 테스트 (선택적, 시간 소요)

생성된 코드가 실제로 컴파일되는지 확인:

1. 클래스 생성 후 에디터 빌드 실행
2. 빌드 성공 여부 확인
3. 생성된 클래스가 에디터에서 인식되는지 확인

---

## 테스트 체크리스트

구현 완료 후 다음 항목을 순서대로 확인:

### 자동화 테스트 (2026-01-18 완료)

- [x] 모든 필수 파일 생성됨 (12개 파일)
- [x] SKILL.md YAML frontmatter 유효함
- [x] Agent 파일 YAML frontmatter 유효함
- [x] 템플릿 파일에 변수 플레이스홀더 포함됨

### 템플릿 생성 테스트 (2026-01-18 완료, D:\BttUnrealEngine)

- [x] Plugin 생성 동작 (TestPlugin 생성 확인)
- [x] Module 생성 동작 (TestModule 생성 확인)
- [x] Actor 클래스 생성 동작 (TestActor 생성 확인)

### 수동 테스트 (2026-01-18 완료, D:\BttUnrealEngine)

- [x] Claude Code에서 스킬 목록에 표시됨
- [x] **경로 질문: 클래스 - 경로 누락 시 최종 경로 질문**
- [x] **경로 질문: 모듈 - 경로 누락 시 플러그인 경로 질문**
- [x] **경로 질문: 플러그인 - 경로 누락 시 생성 위치 질문**
- [x] **경로 질문: 경로 포함 시 질문 없이 바로 진행**
- [x] UObject 클래스 생성 동작 (TestUObject 생성 확인)
- [x] Raw 클래스 생성 동작 (FTestHelper 생성 확인)
- [x] GenerateProjectFiles.bat 실행됨
- [x] 경로 검증: 잘못된 경로 시 에러 메시지 출력
- [x] (선택) 생성된 코드 빌드 성공 (TestUObject, FTestHelper 컴파일 확인)

---

## 구현 시 참고사항

1. **기존 스킬 참고**
   - `unreal-build-skill/SKILL.md`: 스킬 정의 형식
   - `unreal-build-agent.md`: 에이전트 정의 형식

2. **템플릿 변수 규칙**
   - `${ClassName}`: Prefix 없이 순수 클래스명
   - `${ModuleName}`: 모듈 이름
   - `${PluginName}`: 플러그인 이름

3. **파일 생성 위치**
   - 클래스: 현재 모듈의 `Public/` 또는 `Private/` 폴더
   - 모듈: 플러그인의 `Source/` 폴더
   - 플러그인: `Plugins/` 폴더

4. **GenerateProjectFiles 필수**
   - 모든 코드 생성 후 반드시 실행
   - Engine 루트 경로 자동 탐색 필요
