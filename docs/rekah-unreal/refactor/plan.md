# rekah-unreal 리팩토링 Plan

spec: [spec.md](./spec.md)

---

## Step 1: 설정 파일 분리

plugin.json에서 mcpServers, hooks를 분리하고, settings.json을 추가한다.

### 1-1. settings.json 생성

파일: `plugins/rekah-unreal/settings.json`

```json
{
  "enabledMcpjsonServers": ["rekah-unreal"]
}
```

### 1-2. MCP 서버 정의 — plugin.json에 유지

`.mcp.json`에서는 `${CLAUDE_PLUGIN_ROOT}` 등 변수 치환이 안 되는 것으로 확인됨 (knowledge-hub에서도 `.mcp.json`에 경로 변수를 사용하지 않음). 반면 `plugin.json`의 `mcpServers`에서는 변수 치환이 동작함.

따라서 MCP 서버 정의는 **plugin.json에 유지**하고, command만 로컬 경로로 변경한다.

plugin.json의 mcpServers:
```json
{
  "mcpServers": {
    "rekah-unreal": {
      "command": "uv",
      "args": ["--directory", "${CLAUDE_PLUGIN_ROOT}/mcp-server", "run", "rekah-mcp"]
    }
  }
}
```

> `.mcp.json` 파일은 생성하지 않는다.

### 1-3. hooks/hooks.json 생성

파일: `plugins/rekah-unreal/hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
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

### 1-4. plugin.json 정리

파일: `plugins/rekah-unreal/.claude-plugin/plugin.json`

변경 전:
```json
{
  "name": "rekah-unreal",
  "version": "0.12.0",
  ...
  "mcpServers": { ... },
  "hooks": { ... }
}
```

변경 후:
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

- `mcpServers` 유지 (`.mcp.json`에서 변수 치환 미지원이므로 plugin.json에 유지)
- `mcpServers` command를 `uvx --from git+...` → 로컬 `uv --directory` 로 변경
- `hooks` 제거 → `hooks/hooks.json`으로 이동
- `version` 0.12.0 → 0.13.0

---

## Step 2: MCP 서버 코드 통합

`D:\rekah-unreal-mcp`의 소스코드를 `plugins/rekah-unreal/mcp-server/`로 복사한다.

### 2-1. 복사 대상

```
rekah-unreal-mcp/ → plugins/rekah-unreal/mcp-server/
  ├── pyproject.toml
  ├── config.ini
  ├── config.ini.example
  ├── rekah_mcp/          (전체)
  └── tests/              (전체)
```

### 2-2. 제외 대상

```
.git/
.github/
.claude/
.gitignore              (rekah-plugins 루트에서 관리)
uv.lock                 (이동 후 uv sync로 재생성)
intermediates/           (gitignore 대상)
logs/
docs/refactor/REFACTOR_COMPLETE.md  (이전 리팩토링 완료 문서)
```

### 2-3. docs 이동

```
rekah-unreal-mcp/docs/unreal-bridge/SPEC.md
  → docs/rekah-unreal/unreal-bridge/SPEC.md
```

MCP 서버 내부가 아니라 rekah-plugins docs 레벨로 이동 (향후 기능 스펙).

### 2-4. config.ini 수정

변경 전:
```ini
[test]
test_project_dir = D:/BttUnrealEngine
```

변경 후:
```ini
[test]
test_project_dir = ${UE_PROJECT_DIR:-D:/BttUnrealEngine}
```

> 환경변수 우선, 기본값 유지. 또는 config.ini.example만 남기고 config.ini는 gitignore.

### 2-5. uv sync 실행

```bash
uv --directory plugins/rekah-unreal/mcp-server sync
```

mcp-server/ 내에서 의존성 설치 및 uv.lock 재생성.

---

## Step 3: .gitignore 업데이트

`plugins/rekah-unreal/mcp-server/` 관련 항목을 rekah-plugins 루트 `.gitignore`에 추가:

```gitignore
# MCP server runtime
**/mcp-server/logs/
**/mcp-server/intermediates/
**/mcp-server/.venv/
**/mcp-server/config.ini
```

`config.ini`를 gitignore하고 `config.ini.example`만 커밋.

---

## Step 4: session-start.ps1 업데이트

MCP 서버가 로컬이므로 첫 실행 시 의존성 설치를 보장하는 로직 추가.

변경: `scripts/session-start.ps1`

```powershell
# MCP server dependency check
$McpServerDir = Join-Path $env:CLAUDE_PLUGIN_ROOT "mcp-server"
$VenvDir = Join-Path $McpServerDir ".venv"

if (-not (Test-Path $VenvDir)) {
    Write-Host "[rekah-unreal] First run: installing MCP server dependencies..."
    uv --directory $McpServerDir sync
}
```

기존 Unreal 프로젝트 감지, compile_commands.json 체크 로직은 유지.

---

## Step 5: 동작 검증

### 5-1. 플러그인 로드 검증

```bash
# 마켓플레이스 업데이트
claude plugin marketplace update rekah-plugins

# 플러그인 재설치
claude plugin uninstall rekah-unreal@rekah-plugins
claude plugin install rekah-unreal@rekah-plugins --scope project

# 세션 재시작
exit
claude
```

### 5-2. 검증 항목

| # | 항목 | 확인 방법 |
|---|------|----------|
| 1 | 플러그인 정상 로드 | 세션 시작 시 `[rekah-unreal]` 로그 출력 |
| 2 | SessionStart hook | `session-start.ps1` 실행 확인 |
| 3 | MCP 서버 시작 | `/mcp` 또는 MCP 도구 호출 |
| 4 | `${CLAUDE_PLUGIN_ROOT}` | plugin.json mcpServers에서 경로 치환 확인 |
| 5 | LSP 도구 동작 | `setup_lsp` → `goToDefinition` 테스트 |
| 6 | skills 트리거 | "빌드", "클래스 생성" 등 키워드 테스트 |
| 7 | mcp-server 테스트 | `uv --directory mcp-server run pytest -v` |

---

## Step 6: update-plugin.md 업데이트

MCP 서버가 내장되었으므로 별도 MCP 업데이트 언급 불필요. 기존 내용 유지하되, MCP 서버 관련 참고 사항 추가:

```markdown
> MCP 서버는 플러그인에 내장되어 있으므로 플러그인 업데이트 시 함께 업데이트됩니다.
> 첫 실행 시 `uv sync`로 의존성이 자동 설치됩니다.
```

---

## Step 7: rekah-unreal-mcp 레포 아카이브

통합 완료 후:

1. `D:\rekah-unreal-mcp` README.md에 이전 안내 추가:
   ```
   > This repository has been merged into [rekah-plugins](https://github.com/tkdgur4427/rekah-plugins)
   > under `plugins/rekah-unreal/mcp-server/`.
   ```
2. GitHub에서 레포 아카이브 처리 (Settings → Archive)

---

## 실행 순서 요약

```
Step 1: 설정 파일 분리 (settings.json, hooks/hooks.json, plugin.json 정리)
Step 2: MCP 서버 코드 통합 (복사 + 제외 + docs 이동 + uv sync)
Step 3: .gitignore 업데이트
Step 4: session-start.ps1 업데이트
Step 5: 동작 검증 (플러그인 로드 → MCP → LSP → skills)
Step 6: update-plugin.md 업데이트
Step 7: rekah-unreal-mcp 레포 아카이브
```

Step 1~4는 코드 변경, Step 5는 검증, Step 6~7은 문서/정리.
