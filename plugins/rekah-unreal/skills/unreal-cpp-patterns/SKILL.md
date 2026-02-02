---
name: unreal-cpp-patterns
description: Unreal Engine C++ 코드 작성 시 베스트 프랙티스, 코딩 표준을 안내합니다.
  UObject, AActor, UActorComponent 작성, 메모리 관리, UPROPERTY/UFUNCTION 사용 시 활성화됩니다.
---

# Unreal C++ Patterns

## Coding Standards

| 항목 | 핵심 |
|------|------|
| 네이밍 규칙 | U/A/F/E/I/T 접두사, PascalCase |
| Namespace | 접두사 대신 네임스페이스 |
| UPROPERTY | EditAnywhere, BlueprintReadWrite 등 |
| UFUNCTION | BlueprintCallable, BlueprintPure 등 |
| 객체 생성 | NewObject, CreateDefaultSubobject, SpawnActor |
| 메모리 관리 | GC 관리, TWeakObjectPtr, TUniquePtr |
| 델리게이트 | 불필요한 체인 지양 |
| Enum | namespace + enum Type 패턴 |
| 폴더 구조 | Private 폴더 생략 |
| 접근 제어 | 불필요한 private 지양 |
| 주석 | *왜*만 주석, 영어만 |
| YAGNI | 현재 필요한 것만 작성 |
| Over-Engineering | 가장 단순한 해결책 선택 |

**Reference:** [CODING_STANDARDS.md](./CODING_STANDARDS.md)

---

## Lock Patterns

| 패턴 | 핵심 |
|------|------|
| Coarse-Grained Lock | 클래스당 하나의 FCriticalSection |
| Lock Encapsulation | 접근자로 락 캡슐화 |
| Batch APIs | 배치 연산으로 락 사이클 최소화 |
| Minimal Lock Scope | 로컬 복사 후 락 해제 |

**Reference:** [LOCK_PATTERNS.md](./LOCK_PATTERNS.md)
