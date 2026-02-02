# Unreal C++ Patterns - Update Spec

> `unreal-cpp-patterns` 스킬 업데이트 명세 - **완료됨**

---

## Status: Completed

**완료일:** 2026-02-02

---

## 변경 요약

### 1. unreal-build-agent.md 업데이트

**파일:** `plugins/rekah-unreal/agents/unreal-build-agent.md`

추가된 섹션:

| 섹션 | 내용 |
|------|------|
| UnrealEditor.exe 종료 확인 | 에디터 타겟 빌드 전 프로세스 확인 필수 |
| 풀빌드 방지 | `-Rebuild`, `-Clean` 사용 금지, 경로 일관성 유지 |
| 플러그인 빌드 | 플러그인 개별 빌드 금지, 프로젝트 빌드로 대체 |

수정된 내용:
- 추가 빌드 옵션 테이블에 "주의" 컬럼 추가
- `-Rebuild`, `-Clean`에 **사용 금지** 경고 표시

---

### 2. unreal-cpp-patterns 스킬 Restructuring

**폴더:** `plugins/rekah-unreal/skills/unreal-cpp-patterns/`

#### Before
```
unreal-cpp-patterns/
├── SKILL.md              # 핵심 규칙 상세
└── CODING_STANDARDS.md   # 네이밍, UPROPERTY, UFUNCTION
```

#### After
```
unreal-cpp-patterns/
├── SKILL.md              # TOC (요약 테이블 + Reference)
├── CODING_STANDARDS.md   # 기존 + Best Practices 1-8 통합
└── LOCK_PATTERNS.md      # Lock Patterns 1-4 (새로 생성)
```

---

## 적용된 패턴 상세

### CODING_STANDARDS.md에 추가된 내용

| # | 패턴 | 섹션 |
|---|------|------|
| 1 | Avoid Over-Engineering | Avoid Over-Engineering |
| 2 | Use Namespace Instead of Prefix | 네이밍 규칙 > Use Namespace Instead of Prefix |
| 3 | Minimize Comments | 주석 |
| 4 | YAGNI | YAGNI (You Aren't Gonna Need It) |
| 5 | Use Public Folder Only | 폴더 구조 |
| 6 | Keep Class Members Public | 접근 제어 |
| 7 | Avoid Premature Delegate Chains | 델리게이트 > Avoid Premature Delegate Chains |
| 8 | Use Unreal-Style Namespace Enum | Enum 스타일 |

### LOCK_PATTERNS.md (새로 생성)

| # | 패턴 | 핵심 |
|---|------|------|
| 1 | Coarse-Grained Lock | 클래스당 하나의 FCriticalSection |
| 2 | Lock Encapsulation | 접근자로 락 캡슐화 |
| 3 | Batch APIs | 배치 연산으로 락 사이클 최소화 |
| 4 | Minimal Lock Scope | 로컬 복사 후 락 해제 |

---

## SKILL.md 최종 구조

```markdown
# Unreal C++ Patterns

## Coding Standards
| 항목 | 핵심 |
| ... | ... |
**Reference:** CODING_STANDARDS.md

## Lock Patterns
| 패턴 | 핵심 |
| ... | ... |
**Reference:** LOCK_PATTERNS.md
```

---

## Original Spec (Reference)

### 패턴 목록

#### 1. Avoid Over-Engineering
- 가장 단순한 해결책 선택
- 설정이 자주 변경되지 않으면 상수로 충분
- 추상화 레이어는 구체적인 이점이 있을 때만

#### 2. Use Namespace Instead of Prefix
- 일반 C++ 클래스는 네임스페이스로 스코핑
- UCLASS/USTRUCT는 네임스페이스 사용 불가 (UE 제약)

#### 3. Minimize Comments
- *무엇을*이 아닌 *왜*를 설명할 때만 주석
- 영어 주석만 사용

#### 4. YAGNI (You Aren't Gonna Need It)
- 현재 필요한 것만 작성
- 특수 멤버 함수는 필요할 때만 구현
- 에러 코드, 상수는 해당 기능 구현 시 추가

#### 5. Use Public Folder Only
- 단일 모듈 플러그인은 Private 폴더 생략
- 다른 모듈에 구현 숨길 때만 Private 추가

#### 6. Keep Class Members Public
- 불변성 깨뜨리는 세부사항에만 private 사용
- 모듈 레벨 클래스는 엄격한 캡슐화 불필요

#### 7. Avoid Premature Delegate Chains
- 델리게이트는 모듈 분리 또는 외부 소비자 알림용
- 단일 모듈 내에서는 직접 처리

#### 8. Use Unreal-Style Namespace Enum
- `namespace EName { enum Type { ... }; }` 패턴
- enum class 대신 UE 스타일 사용

#### 9. Lock Patterns
- 9.1: Coarse-Grained Lock - 클래스당 단일 락
- 9.2: Lock Encapsulation - 접근자로 캡슐화
- 9.3: Batch APIs - 배치 연산으로 락 사이클 최소화
- 9.4: Minimal Lock Scope - 로컬 복사 후 락 해제

---

## Notes

- 모든 가이드라인은 간결성과 유지보수성 증진 목표
- Unreal Engine 특화 패턴과 흔한 함정에 집중
- YAGNI (You Aren't Gonna Need It) 원칙 강력 적용
- 피드백을 통해 필요한 항목은 독립 md로 분리 예정
