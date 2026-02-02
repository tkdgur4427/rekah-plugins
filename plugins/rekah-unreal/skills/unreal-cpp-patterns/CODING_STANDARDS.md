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

### Use Namespace Instead of Prefix

일반 C++ 클래스는 장황한 접두사 대신 네임스페이스로 스코핑.

```cpp
// Bad
class FRekahTcpConnection { };
class FRekahTcpServer { };

// Good
namespace Rekah
{
    class FTcpConnection { };
    class FTcpServer { };
}
```

> UCLASS/USTRUCT는 네임스페이스 사용 불가 (UE 제약)

---

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

---

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

---

## 객체 생성

| 함수 | 용도 |
|------|------|
| `NewObject<T>()` | 런타임 객체 생성 |
| `CreateDefaultSubobject<T>()` | 컴포넌트 생성 (생성자에서만) |
| `SpawnActor<T>()` | 월드에 액터 스폰 |

### 생성자 패턴

```cpp
AMyActor::AMyActor()
{
    PrimaryActorTick.bCanEverTick = true;

    RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    MeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
    MeshComponent->SetupAttachment(RootComponent);
}
```

---

## 메모리 관리

- UObject 상속 클래스는 GC가 관리 → `delete` 사용 금지
- `TWeakObjectPtr<T>` - 약한 참조
- `TSharedPtr<T>` / `TUniquePtr<T>` - 비 UObject용

---

## 델리게이트

### 선언
```cpp
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnHealthChanged, float, NewHealth);

UPROPERTY(BlueprintAssignable, Category = "Events")
FOnHealthChanged OnHealthChanged;
```

### 브로드캐스트
```cpp
OnHealthChanged.Broadcast(CurrentHealth);
```

### Avoid Premature Delegate Chains

델리게이트는 모듈 분리 또는 외부 소비자 알림용. 단일 모듈 내에서는 직접 메서드 호출이나 리턴 값 사용.

```cpp
// Bad - 불필요한 델리게이트 체인
class FTcpConnection {
    FOnDataReceived OnDataReceived;
};

// Good - 직접 처리
class FTcpConnection {
    bool Tick(FString& OutMessage);  // 데이터 직접 리턴
};
```

---

## Enum 스타일

UE는 `namespace EName { enum Type { ... }; }` 패턴 사용.

```cpp
// Bad
enum class EParseState : uint8 { ReadingHeader, ReadingBody };

// Good
namespace EParseState
{
    enum Type { ReadingHeader, ReadingBody };
}
// 사용: EParseState::ReadingHeader
// 파라미터 타입: EParseState::Type
```

---

## 폴더 구조

단일 모듈 플러그인은 `Private/` 폴더 생략. 모든 코드를 `Public/`에 배치.

```
// Bad
Source/MyPlugin/
├── Public/
│   └── MyClass.h
└── Private/
    └── MyClass.cpp

// Good
Source/MyPlugin/
├── MyPlugin.Build.cs
└── Public/
    ├── MyClass.h
    └── MyClass.cpp
```

> 다른 모듈에 구현을 숨겨야 할 때만 `Private/` 추가

---

## 접근 제어

불변성을 깨뜨릴 수 있는 구현 세부사항에만 `private:` 사용. 모듈 레벨 클래스는 엄격한 캡슐화 불필요.

```cpp
// Bad
class FMyModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
private:  // 불필요한 숨김
    void StartServer();
    TUniquePtr<FServer> Server;
};

// Good
class FMyModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    void StartServer();
    TUniquePtr<FServer> Server;
};
```

---

## 주석

*무엇을*이 아닌 *왜*를 설명할 때만 주석 추가. 영어 주석만 사용.

```cpp
// Bad
// The port number for the server
int32 ServerPort = 9876;

// Good
int32 ServerPort = 9876;

// Workaround for UE5.3 socket bug where Recv returns -1 on graceful close
if (BytesRead < 0 && LastError == SE_EWOULDBLOCK) { ... }
```

---

## YAGNI (You Aren't Gonna Need It)

현재 구현에서 실제로 사용하는 것만 작성.

**고려사항:**
- 미리 작성된 코드는 실제 요구사항과 맞지 않을 수 있음
- 미사용 코드는 유지보수 부담
- 필요해지면 그때 추가하는 것이 더 정확함

```cpp
// Bad - 불필요한 메서드
class FTcpConnection
{
public:
    FTcpConnection(FSocket* InSocket);
    ~FTcpConnection();
    FTcpConnection(FTcpConnection&& Other) noexcept;  // 사용 안 함
    FTcpConnection& operator=(FTcpConnection&&) noexcept;  // 사용 안 함
};

// Good - 필요한 것만
class FTcpConnection
{
public:
    FTcpConnection(FSocket* InSocket);
    ~FTcpConnection();
    FTcpConnection(const FTcpConnection&) = delete;
    FTcpConnection& operator=(const FTcpConnection&) = delete;
};
```

```cpp
// Bad - 미래를 위한 상수
namespace EJsonRpcError
{
    constexpr int32 ParseError = -32700;      // 현재 사용
    constexpr int32 AssetNotFound = -32001;   // 아직 구현 안 됨
    constexpr int32 WindowNotFound = -32002;  // 아직 구현 안 됨
}

// Good - 현재 필요한 것만
namespace EJsonRpcError
{
    constexpr int32 ParseError = -32700;
    // 추가 에러는 해당 기능 구현 시 추가
}
```

---

## Avoid Over-Engineering

가장 단순한 해결책 선택. 설정이 자주 변경되지 않으면 상수로 충분.

```cpp
// Bad - 거의 변경 안 되는 값에 UDeveloperSettings
UCLASS(Config=Engine, DefaultConfig)
class UMySettings : public UDeveloperSettings
{
    UPROPERTY(Config, EditAnywhere)
    int32 ServerPort = 9876;
};

// Good - 단순한 상수
namespace MyPlugin
{
    constexpr int32 DefaultServerPort = 9876;
    constexpr int32 DefaultMaxConnections = 4;
}
```
