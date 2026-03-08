# rekah-unreal 플러그인 리팩토링 Spec

## 배경

### 현재 문제점

1. **rekah-unreal-mcp 별도 관리 부담**: `D:\rekah-unreal-mcp`가 독립 레포로 존재하여 버전 동기화, 배포, 테스트를 이중으로 관리해야 함
2. **plugin.json 과부하**: MCP 서버 정의, hooks, 메타데이터가 모두 plugin.json에 혼재
3. **settings.json 부재**: knowledge-hub-plugin처럼 플러그인 런타임 설정(agent, MCP 활성화)을 분리하지 않음

### 레퍼런스: knowledge-hub-plugin 구조

```
knowledge-hub-plugin/
├── .claude-plugin/plugin.json    # 메타데이터만 (MCP/hooks 없음)
├── .mcp.json                     # MCP 서버 정의 (분리)
├── settings.json                 # agent + enabledMcpjsonServers
├── hooks/hooks.json              # hooks 정의 (분리)
├── agents/
├── commands/
├── scripts/
└── skills/
```

핵심 패턴:
- `plugin.json`은 메타데이터 + mcpServers 담당 (`.mcp.json`에서 `${CLAUDE_PLUGIN_ROOT}` 변수 치환 미지원)
- `settings.json`으로 런타임 설정 분리
- `hooks/hooks.json`으로 훅 정의 분리

---

## 제안: rekah-unreal-mcp를 플러그인에 통합

### 이유

별도 레포로 관리하는 것이 불편함. rekah-unreal-mcp는 rekah-unreal 플러그인 전용이므로 하나로 합치는 게 단순하고 합리적.

### uv 멀티 프로젝트

각 `mcp-server/` 디렉토리가 자체 `pyproject.toml`을 가지면 독립된 Python 프로젝트로 동작한다. `uv --directory <path>` 옵션으로 해당 경로 기준으로 실행하므로, marketplace 내 복수 플러그인이 각자 MCP 서버를 가져도 충돌 없이 관리 가능.

---

## 목표 구조

```
plugins/rekah-unreal/
├── .claude-plugin/
│   └── plugin.json                 # 메타데이터 + mcpServers
├── settings.json                   # 런타임 설정
├── hooks/
│   └── hooks.json                  # hooks 정의 (분리)
│
├── agents/
│   ├── unreal-assistant-agent.md
│   ├── unreal-build-agent.md
│   ├── unreal-code-analysis-agent.md
│   └── unreal-run-agent.md
│
├── commands/
│   └── update-plugin.md
│
├── scripts/
│   ├── session-start.ps1
│   └── setup-project.py
│
├── skills/
│   ├── unreal-assistant/
│   ├── unreal-build-skill/
│   ├── unreal-code-analysis/
│   ├── unreal-cpp-patterns/
│   └── unreal-run-skill/
│
└── mcp-server/                     # rekah-unreal-mcp 통합
    ├── pyproject.toml
    ├── config.ini
    ├── config.ini.example
    ├── rekah_mcp/
    │   ├── __init__.py
    │   ├── server.py
    │   ├── tools/
    │   │   └── tools_utils.py
    │   ├── lsp/
    │   │   └── lsp_utils.py
    │   └── utils/
    │       ├── singleton_utils.py
    │       ├── config_utils.py
    │       └── logging_utils.py
    ├── tests/
    │   └── test_lsp_utils.py
    └── docs/
        └── unreal-bridge/
            └── SPEC.md
```

---

## 변경 상세

### P0: 설정 파일 분리

#### 1. plugin.json - 메타데이터 + mcpServers

`.mcp.json`에서는 `${CLAUDE_PLUGIN_ROOT}` 변수 치환이 안 되므로, mcpServers는 plugin.json에 유지한다. command만 로컬 경로로 변경.

```json
{
  "name": "rekah-unreal",
  "version": "0.13.0",
  "description": "Unreal Engine 개발을 위한 Claude Code 플러그인",
  "author": { "name": "Haker" },
  "repository": "https://github.com/tkdgur4427/rekah-plugins",
  "keywords": ["unreal", "cpp", "gamedev", "lsp", "clangd"],
  "mcpServers": {
    "rekah-unreal": {
      "command": "uv",
      "args": ["--directory", "${CLAUDE_PLUGIN_ROOT}/mcp-server", "run", "rekah-mcp"]
    }
  }
}
```

#### 2. settings.json - 런타임 설정

```json
{
  "enabledMcpjsonServers": ["rekah-unreal"]
}
```

> Note: `agent` 필드는 현재 기본 agent를 지정할 필요가 없으므로 생략. 필요시 추가.

#### 3. hooks/hooks.json - hooks 분리

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"${CLAUDE_PLUGIN_ROOT}/scripts/session-start.ps1\"",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### P1: MCP 서버 통합

1. `D:\rekah-unreal-mcp` 내용을 `plugins/rekah-unreal/mcp-server/`로 이동
2. 불필요 파일 제외:
   - `.git/`, `.github/` (CI는 rekah-plugins 쪽에서 관리)
   - `.claude/` (플러그인 루트 설정 사용)
   - `uv.lock` (이동 후 재생성)
   - `docs/refactor/REFACTOR_COMPLETE.md` (이전 리팩토링 완료 문서)
3. `pyproject.toml` 경로 조정 필요 없음 (독립 Python 패키지로 동작)
4. `config.ini` [test] 섹션의 `test_project_dir` 경로를 상대 경로나 환경변수로 변경

### P2: session-start.ps1 업데이트

MCP 서버가 로컬로 변경되었으므로 관련 스크립트 수정:
- `uvx` 기반 MCP 실행 참조가 있다면 로컬 경로로 변경
- `uv sync` 등 초기 의존성 설치 단계 추가 (첫 실행 시)

### P3: update-plugin.md 업데이트

MCP 서버가 플러그인에 내장되므로 별도 MCP 서버 업데이트 절차 불필요.
플러그인 업데이트 = MCP 서버 업데이트.

---

## 마이그레이션 순서

```
Step 1: settings.json, .mcp.json, hooks/hooks.json 생성
Step 2: plugin.json에서 mcpServers, hooks 제거 (메타데이터만 남김)
Step 3: mcp-server/ 디렉토리 생성 및 rekah-unreal-mcp 코드 복사
Step 4: .mcp.json의 MCP 서버 command를 로컬 경로로 변경
Step 5: session-start.ps1 업데이트
Step 6: 동작 확인 (MCP 서버 시작, LSP 도구 호출)
Step 7: rekah-unreal-mcp 레포 아카이브 (README에 이전 안내)
```

---

## 검증 체크리스트

- [ ] `claude plugin update` 후 플러그인 정상 로드
- [ ] MCP 서버(`rekah-unreal`) 정상 시작
- [ ] LSP 도구 12개 모두 동작 (setup_lsp, goToDefinition 등)
- [ ] SessionStart hook 정상 실행
- [ ] skills 4개 모두 정상 트리거
- [ ] agents 4개 모두 정상 동작
- [ ] `uv run pytest` mcp-server/ 테스트 통과

---

## 미해결 사항

1. **CI/CD**: rekah-unreal-mcp의 GitHub Actions(test.yml, release.yml)을 rekah-plugins 레벨로 이전할지 결정
2. **PyPI 배포 중단**: 통합 후 독립 PyPI 배포가 불필요하므로 release.yml 제거 여부 결정
3. **unreal-bridge SPEC**: `mcp-server/docs/unreal-bridge/SPEC.md`는 향후 기능 스펙이므로 `docs/rekah-unreal/`로 이동하는 것이 나을 수 있음
