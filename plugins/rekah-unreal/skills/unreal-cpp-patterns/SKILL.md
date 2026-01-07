---
name: unreal-cpp-patterns
description: Unreal Engine C++ 코드 작성 시 베스트 프랙티스, 코딩 표준을 안내합니다.
  UObject, AActor, UActorComponent 작성, 메모리 관리, UPROPERTY/UFUNCTION 사용 시 활성화됩니다.
---

# Unreal C++ Patterns

이 skill은 Unreal Engine C++ 개발 패턴을 안내합니다.

## 핵심 규칙

### 매크로 사용
- 모든 리플렉션 프로퍼티에 `UPROPERTY()` 매크로 필수
- 블루프린트 노출 함수에 `UFUNCTION()` 매크로 필수
- 클래스 선언에 `UCLASS()` 매크로 필수

### 객체 생성
- `NewObject<T>()` - 런타임 객체 생성
- `CreateDefaultSubobject<T>()` - 컴포넌트 생성 (생성자에서만)
- `SpawnActor<T>()` - 월드에 액터 스폰

### 메모리 관리
- UObject 상속 클래스는 GC가 관리 → `delete` 사용 금지
- `TWeakObjectPtr<T>` - 약한 참조
- `TSharedPtr<T>` / `TUniquePtr<T>` - 비 UObject용

상세 코딩 표준은 [CODING_STANDARDS.md](./CODING_STANDARDS.md) 참조
