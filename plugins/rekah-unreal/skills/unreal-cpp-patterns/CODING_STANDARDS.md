# Unreal Engine C++ 코딩 표준

## 네이밍 규칙

### 클래스 접두사
| 접두사 | 용도 | 예시 |
|--------|------|------|
| `U` | UObject 상속 클래스 | `UMyComponent` |
| `A` | AActor 상속 클래스 | `AMyCharacter` |
| `F` | 구조체, 비 UObject 클래스 | `FMyStruct` |
| `E` | enum | `EMyEnum` |
| `I` | 인터페이스 | `IMyInterface` |
| `T` | 템플릿 | `TArray`, `TMap` |

### 멤버 변수
- 포인터가 아닌 경우: PascalCase
- UPROPERTY 노출 시: PascalCase

```cpp
UPROPERTY(EditAnywhere)
float MaxHealth;

UPROPERTY(VisibleAnywhere)
UStaticMeshComponent* MeshComponent;
```

## UPROPERTY 지정자

### 에디터 노출
| 지정자 | 설명 |
|--------|------|
| `EditAnywhere` | 인스턴스 + 블루프린트 클래스에서 편집 |
| `EditDefaultsOnly` | 블루프린트 클래스에서만 편집 |
| `EditInstanceOnly` | 인스턴스에서만 편집 |
| `VisibleAnywhere` | 읽기 전용으로 표시 |

### 블루프린트 노출
| 지정자 | 설명 |
|--------|------|
| `BlueprintReadWrite` | 읽기/쓰기 가능 |
| `BlueprintReadOnly` | 읽기만 가능 |

### 카테고리
```cpp
UPROPERTY(EditAnywhere, Category = "Combat|Stats")
float AttackPower;
```

## UFUNCTION 지정자

### 블루프린트 노출
| 지정자 | 설명 |
|--------|------|
| `BlueprintCallable` | BP에서 호출 가능 |
| `BlueprintPure` | 순수 함수 (사이드 이펙트 없음) |
| `BlueprintImplementableEvent` | BP에서 구현 |
| `BlueprintNativeEvent` | C++ 기본 구현 + BP 오버라이드 |

### 예시
```cpp
UFUNCTION(BlueprintCallable, Category = "Combat")
void TakeDamage(float DamageAmount);

UFUNCTION(BlueprintPure, Category = "Stats")
float GetHealthPercent() const;
```

## 생성자 패턴

```cpp
AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true;

    // 컴포넌트 생성
    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    MeshComponent->SetupAttachment(RootComponent);
}
```

## 델리게이트

### 선언
```cpp
// 단일 파라미터
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealthChanged, float, NewHealth);

// 클래스 내부
UPROPERTY(BlueprintAssignable, Category = "Events")
FOnHealthChanged OnHealthChanged;
```

### 브로드캐스트
```cpp
OnHealthChanged.Broadcast(CurrentHealth);
```
