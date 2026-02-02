# Unreal C++ Lock Patterns

## 1. Prefer Coarse-Grained Lock

클래스당 단일 `FCriticalSection SyncObject` 사용. 다중 락은 순서 문제와 데드락 유발.

```cpp
// Bad
class FTcpServer
{
    FCriticalSection ConnectionsLock;
    FCriticalSection PendingLock;

    void Process() {
        FScopeLock Lock1(&ConnectionsLock);
        FScopeLock Lock2(&PendingLock);  // 잠재적 데드락
    }
};

// Good
class FTcpServer
{
    FCriticalSection SyncObject;  // 단일 락

    void Process() {
        FScopeLock Lock(&SyncObject);
    }
};
```

---

## 2. Encapsulate Lock with Accessors

공유 데이터와 락을 protected/private으로 이동. 내부적으로 락을 처리하는 public 접근자 제공.

```cpp
// Bad
class FTcpServer
{
public:
    FCriticalSection SyncObject;
    TMap<uint32, TUniquePtr<FConnection>> Connections;

    void DoSomething() {
        FScopeLock Lock(&SyncObject);  // 잊기 쉬움!
        Connections.Add(...);
    }
};

// Good
class FTcpServer
{
public:
    void AddConnection(uint32 Id, TUniquePtr<FConnection> Conn);
    int32 GetConnectionCount() const;

protected:
    FCriticalSection SyncObject;
    TMap<uint32, TUniquePtr<FConnection>> Connections;
};

void FTcpServer::AddConnection(uint32 Id, TUniquePtr<FConnection> Conn)
{
    FScopeLock Lock(&SyncObject);
    Connections.Add(Id, MoveTemp(Conn));
}
```

---

## 3. Prefer Batch APIs for Locked Operations

단일 항목 API는 여러 항목 처리 시 반복적인 lock/unlock 사이클 발생. 락 획득 비용: 시스콜 + 캐시 무효화.

```cpp
// Bad - 4개 연결 = 4번 락 사이클
for (auto& Socket : NewSockets) {
    AddConnection(Socket);
}

// Good - 4개 연결 = 1번 락 사이클
TArray<uint32> NewIds = AddConnections(NewSockets);
```

---

## 4. Minimize Lock Scope with Local Copies

비싼 연산 (처리, 로깅, I/O) 중에 락 유지 금지. 공유 데이터를 로컬 변수로 복사할 때만 락.

```cpp
// Bad
bool FTcpServer::Tick(float DeltaTime)
{
    FScopeLock Lock(&SyncObject);
    for (auto& Pair : Connections) {
        FString Msg;
        if (Pair.Value->Tick(Msg)) {
            UE_LOG(...);           // 락 중 I/O
            ProcessMessage(Msg);   // 락 중 무거운 작업
        }
    }
    return true;
}

// Good
bool FTcpServer::Tick(float DeltaTime)
{
    TArray<TPair<uint32, FString>> Messages;
    {
        FScopeLock Lock(&SyncObject);
        for (auto& Pair : Connections) {
            FString Msg;
            if (Pair.Value->Tick(Msg) && !Msg.IsEmpty()) {
                Messages.Add({Pair.Key, Msg});
            }
        }
    }
    // 락 없이 처리
    for (const auto& [Id, Msg] : Messages) {
        UE_LOG(...);
        ProcessMessage(Msg);
    }
    return true;
}
```

---

## Summary

| # | 패턴 | 핵심 |
|---|------|------|
| 1 | Coarse-Grained Lock | 클래스당 하나의 FCriticalSection |
| 2 | Lock Encapsulation | 접근자로 락 캡슐화 |
| 3 | Batch APIs | 배치 연산으로 락 사이클 최소화 |
| 4 | Minimal Lock Scope | 로컬 복사 후 락 해제 |
