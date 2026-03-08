# Unreal Bridge MCP Specification

> Version: 0.1.0
> Target: Unreal Engine 5.3+
> Protocol: TCP Socket with LSP/MCP-compatible JSON-RPC 2.0
> Plugin Repo: `D:\RekahUnrealBridgeMCP` (Symbolic Link to game project)
>
> **구현 상태:**
> - ✅ TCP 서버 (Plan 02 완료 - 2026-01-31)
> - 📝 JSON-RPC 핸들러 (Plan 03 예정)
> - 📝 MCP Tools (Plan 04+ 예정)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [MCP Tools](#3-mcp-tools)
4. [Protocol](#4-protocol)
5. [Plugin Implementation Guide](#5-plugin-implementation-guide)

---

## 1. Overview

### 1.1 Purpose

Unreal Bridge MCP는 Claude가 Unreal Engine Editor를 직접 제어할 수 있게 하는 MCP(Model Context Protocol) 서버입니다. Chrome MCP가 웹 브라우저를 자동화하는 것처럼, 이 시스템은 게임 개발 워크플로우를 자동화합니다.

**핵심 컨셉**: 웹 브라우저 자동화처럼 **위젯 기반 상호작용**으로 에디터를 제어합니다. Widget Reflector 패턴을 참고하여, 스크린샷 + 위젯 트리를 활용한 시각적 자동화를 지원합니다.

**주요 사용 사례:**
- 에디터 창/탭 상태 파악 및 전환
- 위젯 기반 UI 상호작용 (클릭, 입력)
- 에셋 검색 및 열기
- 스크린샷 캡처 및 문서화
- 로그 분석

### 1.2 Design Principles

1. **최소 기능 원칙**: 핵심 기능만 구현, 필요시 확장
2. **위젯 기반 상호작용**: Chrome MCP의 DOM 접근처럼 Slate 위젯 트리 활용
3. **GameThread 안전성**: 모든 에디터 조작은 GameThread에서 실행
4. **비파괴적 기본값**: 읽기 작업은 자유롭게, 쓰기 작업은 명시적

### 1.3 Integration with Existing rekah_mcp

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐    ┌─────────────────────┐         │
│  │   rekah_mcp         │    │   unreal-bridge     │         │
│  │   (LSP Tools)       │    │   (Editor Tools)    │         │
│  │                     │    │                     │         │
│  │  - workspace/symbols│    │  - editor_context   │         │
│  │  - goto/definition  │    │  - read_widget_tree │         │
│  │  - find/references  │    │  - click_widget     │         │
│  │  - diagnostics      │    │  - find_assets      │         │
│  │  - hover            │    │  - capture_window   │         │
│  └──────────┬──────────┘    └──────────┬──────────┘         │
│             │                          │                     │
│             ▼                          ▼                     │
│  ┌─────────────────────┐    ┌─────────────────────┐         │
│  │     clangd          │    │   UE Editor Plugin  │         │
│  │     (LSP Server)    │    │   (TCP Server)      │         │
│  └─────────────────────┘    └─────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MCP Client (Claude)                          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ MCP Protocol (stdio)
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Python MCP Server                                │
│                     (unreal_bridge module)                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Tool Handlers (8 Core Tools)                                │    │
│  │  - Context: editor_context                                   │    │
│  │  - Navigation: focus_window                                  │    │
│  │  - Read: read_details_panel                                  │    │
│  │  - Search: find_assets                                       │    │
│  │  - Widget: read_widget_tree, click_widget                    │    │
│  │  - Debug: read_log                                           │    │
│  │  - Media: capture_window                                     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│                              │ TCP Socket (localhost:9876)           │
│                              │ JSON-RPC 2.0                          │
│                              ▼                                       │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ TCP Connection
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Unreal Engine 5.3+ Editor                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  RekahUnrealBridgeMCP Plugin (Editor Module)                │    │
│  │  ┌────────────────────────┐  ┌────────────────────────┐    │    │
│  │  │ Rekah::FTcpMcpServer   │  │ FRekahUnrealBridgeMCP  │    │    │
│  │  │ (FRunnable + Ticker)   │  │ Module                 │    │    │
│  │  └───────────┬────────────┘  └───────────┬────────────┘    │    │
│  │              │                           │                  │    │
│  │              ▼                           ▼                  │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │ Rekah::FTcpMcpConnection (LSP/MCP Protocol)         │    │    │
│  │  │ + RekahJsonRpcHandler (Plan 03 예정)                │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│                              ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Unreal Editor APIs                                          │    │
│  │  - FSlateApplication, SWidget                                │    │
│  │  - FGlobalTabmanager, SDockTab                               │    │
│  │  - IAssetRegistry, FAssetData                                │    │
│  │  - FWidgetReflectorNodeBase (Widget Reflector 패턴)          │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Widget-Based Interaction Model

Chrome MCP가 HTML DOM을 통해 웹 페이지와 상호작용하듯이, Unreal Bridge는 **Slate Widget Tree**를 통해 에디터와 상호작용합니다.

```
Chrome MCP                          Unreal Bridge MCP
─────────────────────────────────────────────────────────
HTML DOM                    →       Slate Widget Tree
document.querySelector()    →       read_widget_tree
element.click()             →       click_widget
element.textContent         →       widget text/value
DevTools Elements Panel     →       Widget Reflector
```

### 2.3 Connection Management

- **Default Port**: 9876 (설정 가능)
- **Max Connections**: 4
- **Connection Model**: Multiple clients, persistent connections
- **Reconnection**: MCP 서버가 연결 끊김 시 자동 재연결 시도 (최대 5회, 2초 간격)
- **Heartbeat**: 30초마다 `ping` 메시지로 연결 상태 확인
- **Protocol**: LSP/MCP 호환 (`Content-Length: N\r\n\r\n<JSON>`)

---

## 3. MCP Tools

### 3.1 Tool Summary

| Category | Tool | Description | Chrome MCP Equivalent |
|----------|------|-------------|----------------------|
| Context | `editor_context` | 현재 포커스된 창/탭 정보 | `tabs_context_mcp` |
| Navigation | `focus_window` | 창/탭 간 포커스 전환 | `navigate` |
| Read | `read_details_panel` | 포커스된 항목의 Details Panel | `get_page_text` |
| Search | `find_assets` | Content Browser 에셋 검색 | `find` |
| Widget | `read_widget_tree` | 위젯 트리 구조 (Widget Reflector) | `read_page` |
| Widget | `click_widget` | 위젯 클릭 | `computer` (click) |
| Debug | `read_log` | Output Log 읽기 | `read_console_messages` |
| Media | `capture_window` | 활성 창/탭 캡처 | `computer` (screenshot) |

**Total: 8 Core Tools**

---

### 3.2 Context Tools

#### `editor_context`

현재 에디터 상태와 **포커스된 창/탭 정보**를 반환합니다. 이것이 가장 중요한 도구입니다.

**Parameters**: None

**Returns**:
```json
{
  "connected": true,
  "engine_version": "5.3.2",
  "project_name": "MyGame",

  "focused_window": {
    "window_id": "win_1",
    "title": "BP_Player",
    "type": "BlueprintEditor",
    "asset_path": "/Game/Blueprints/BP_Player",
    "is_asset_editor": true
  },

  "open_windows": [
    {
      "window_id": "win_0",
      "title": "Level Editor",
      "type": "LevelEditor",
      "is_main_window": true
    },
    {
      "window_id": "win_1",
      "title": "BP_Player",
      "type": "BlueprintEditor",
      "asset_path": "/Game/Blueprints/BP_Player",
      "is_focused": true
    },
    {
      "window_id": "win_2",
      "title": "M_Character",
      "type": "MaterialEditor",
      "asset_path": "/Game/Materials/M_Character",
      "is_focused": false
    },
    {
      "window_id": "win_3",
      "title": "ABP_Character",
      "type": "AnimationBlueprintEditor",
      "asset_path": "/Game/Animations/ABP_Character",
      "is_focused": false
    }
  ],

  "open_tabs": [
    {
      "tab_id": "tab_1",
      "parent_window": "win_1",
      "label": "Event Graph",
      "is_active": true
    },
    {
      "tab_id": "tab_2",
      "parent_window": "win_1",
      "label": "Components",
      "is_active": false
    }
  ],

  "current_level": "/Game/Maps/MainLevel",
  "pie_state": "stopped"
}
```

**Window Types**:
| Type | Description |
|------|-------------|
| `LevelEditor` | 메인 레벨 에디터 |
| `BlueprintEditor` | 블루프린트 에디터 |
| `MaterialEditor` | 머티리얼 에디터 |
| `AnimationBlueprintEditor` | 애니메이션 블루프린트 |
| `AnimationEditor` | 애니메이션 시퀀스 |
| `StaticMeshEditor` | 스태틱 메시 에디터 |
| `SkeletalMeshEditor` | 스켈레탈 메시 에디터 |
| `TextureEditor` | 텍스처 뷰어 |
| `ContentBrowser` | 콘텐츠 브라우저 |
| `OutputLog` | 출력 로그 |
| `WorldSettings` | 월드 세팅 |
| `Other` | 기타 |

**Example**:
```python
# Check which window has focus
result = await client.call_tool("editor_context", {})
focused = result["focused_window"]
print(f"Currently editing: {focused['title']} ({focused['type']})")

# List all open Blueprint editors
bp_editors = [w for w in result["open_windows"] if w["type"] == "BlueprintEditor"]
```

---

### 3.3 Navigation Tools

#### `focus_window`

특정 창/탭으로 포커스를 전환합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `window_id` | string | Yes* | `editor_context`에서 받은 창 ID |
| `tab_id` | string | Yes* | 특정 탭으로 전환 |
| `asset_path` | string | Yes* | 에셋 경로로 창 찾기/열기 |

*셋 중 하나는 필수. `asset_path` 지정 시 해당 에셋이 열려있으면 포커스, 없으면 새로 열기

**Returns**:
```json
{
  "success": true,
  "focused_window": {
    "window_id": "win_2",
    "title": "M_Character",
    "type": "MaterialEditor",
    "asset_path": "/Game/Materials/M_Character"
  },
  "action": "focused"
}
```

**Action Values**:
- `"focused"`: 기존 창으로 포커스 이동
- `"opened"`: 새 창을 열고 포커스
- `"tab_activated"`: 탭 활성화

**Example**:
```python
# Focus by window ID
await client.call_tool("focus_window", {"window_id": "win_2"})

# Focus by asset (opens if not already open)
await client.call_tool("focus_window", {
    "asset_path": "/Game/Blueprints/BP_Enemy"
})

# Switch to specific tab within a window
await client.call_tool("focus_window", {"tab_id": "tab_2"})
```

---

### 3.4 Read Tools

#### `read_details_panel`

현재 포커스된 창에서 선택된 항목의 Details Panel 정보를 반환합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `category_filter` | string | No | 특정 카테고리만 필터링 |
| `property_filter` | string | No | 속성 이름 필터 (regex) |
| `include_defaults` | boolean | No | 기본값 포함 (default: false) |

**Returns**:
```json
{
  "context": {
    "window_type": "BlueprintEditor",
    "asset_path": "/Game/Blueprints/BP_Player",
    "selected_item": "CharacterMovement0",
    "selected_type": "CharacterMovementComponent"
  },

  "categories": [
    {
      "name": "Character Movement: Walking",
      "properties": [
        {
          "name": "MaxWalkSpeed",
          "display_name": "Max Walk Speed",
          "type": "float",
          "value": 600.0,
          "editable": true
        },
        {
          "name": "MaxWalkSpeedCrouched",
          "display_name": "Max Walk Speed Crouched",
          "type": "float",
          "value": 300.0,
          "editable": true
        }
      ]
    },
    {
      "name": "Character Movement: Jumping / Falling",
      "properties": [
        {
          "name": "JumpZVelocity",
          "display_name": "Jump Z Velocity",
          "type": "float",
          "value": 420.0,
          "editable": true
        }
      ]
    }
  ],

  "total_properties": 45,
  "returned_properties": 45
}
```

**Notes**:
- 포커스된 창 유형에 따라 선택 컨텍스트가 다름:
  - LevelEditor: 선택된 액터
  - BlueprintEditor: Components 패널에서 선택된 컴포넌트
  - MaterialEditor: 선택된 노드

---

### 3.5 Search Tools

#### `find_assets`

Content Browser에서 에셋을 검색합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | No | 이름 검색 (부분 일치) |
| `class_name` | string | No | 에셋 클래스 필터 |
| `path` | string | No | 검색 경로 제한 |
| `recursive` | boolean | No | 하위 폴더 포함 (default: true) |
| `max_results` | number | No | 최대 결과 수 (default: 50) |

**Class Name Options**:
- `Blueprint`
- `AnimBlueprint`
- `Material`
- `MaterialInstance`
- `StaticMesh`
- `SkeletalMesh`
- `Texture2D`
- `SoundWave`
- `World` (Level)
- 기타 UE 에셋 클래스

**Returns**:
```json
{
  "total_found": 12,
  "returned": 12,
  "assets": [
    {
      "path": "/Game/Blueprints/BP_Player",
      "name": "BP_Player",
      "class": "Blueprint",
      "parent_class": "Character"
    },
    {
      "path": "/Game/Blueprints/BP_Enemy",
      "name": "BP_Enemy",
      "class": "Blueprint",
      "parent_class": "Character"
    }
  ]
}
```

**Example**:
```python
# Find all Blueprints with "Player" in name
await client.call_tool("find_assets", {
    "query": "Player",
    "class_name": "Blueprint"
})

# Find all Materials in a specific folder
await client.call_tool("find_assets", {
    "class_name": "Material",
    "path": "/Game/Materials/Characters"
})
```

---

### 3.6 Widget Tools

Widget Reflector 패턴을 활용하여 에디터 UI와 상호작용합니다.

#### `read_widget_tree`

현재 포커스된 창의 위젯 트리를 반환합니다. Chrome MCP의 `read_page`에 대응합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `window_id` | string | No | 특정 창 (default: 포커스된 창) |
| `depth` | number | No | 탐색 깊이 (default: 10) |
| `filter` | string | No | `"interactive"`, `"all"` (default: "interactive") |
| `ref_id` | string | No | 특정 위젯의 하위만 탐색 |

**Returns**:
```json
{
  "window_id": "win_1",
  "window_title": "BP_Player",
  "widget_count": 156,
  "widgets": [
    {
      "ref_id": "w_1",
      "type": "SButton",
      "text": "Compile",
      "bounds": {"x": 100, "y": 50, "width": 80, "height": 24},
      "enabled": true,
      "visible": true,
      "interactive": true,
      "children": []
    },
    {
      "ref_id": "w_2",
      "type": "SButton",
      "text": "Save",
      "bounds": {"x": 190, "y": 50, "width": 60, "height": 24},
      "enabled": true,
      "visible": true,
      "interactive": true,
      "children": []
    },
    {
      "ref_id": "w_3",
      "type": "STreeView",
      "text": "",
      "bounds": {"x": 0, "y": 100, "width": 300, "height": 500},
      "enabled": true,
      "visible": true,
      "interactive": true,
      "children": [
        {
          "ref_id": "w_4",
          "type": "STableRow",
          "text": "BP_Player (self)",
          "bounds": {"x": 0, "y": 100, "width": 300, "height": 20},
          "enabled": true,
          "visible": true,
          "interactive": true,
          "selected": false
        },
        {
          "ref_id": "w_5",
          "type": "STableRow",
          "text": "CapsuleComponent",
          "bounds": {"x": 20, "y": 120, "width": 280, "height": 20},
          "enabled": true,
          "visible": true,
          "interactive": true,
          "selected": true
        }
      ]
    },
    {
      "ref_id": "w_10",
      "type": "SEditableTextBox",
      "text": "600.0",
      "bounds": {"x": 450, "y": 200, "width": 100, "height": 20},
      "enabled": true,
      "visible": true,
      "interactive": true,
      "property_name": "MaxWalkSpeed"
    }
  ]
}
```

**Widget Types** (Common):
| Type | Description | Interactive |
|------|-------------|-------------|
| `SButton` | 버튼 | Yes |
| `SCheckBox` | 체크박스 | Yes |
| `SEditableTextBox` | 텍스트 입력 | Yes |
| `SComboBox` | 드롭다운 | Yes |
| `SSlider` | 슬라이더 | Yes |
| `STreeView` | 트리 뷰 | Yes |
| `STableRow` | 트리/리스트 항목 | Yes |
| `SListView` | 리스트 뷰 | Yes |
| `STextBlock` | 텍스트 라벨 | No |
| `SImage` | 이미지 | No |
| `SBox`, `SBorder` | 컨테이너 | No |

**Notes**:
- `filter: "interactive"` 사용 시 클릭/입력 가능한 위젯만 반환
- `ref_id`는 세션 내에서 유효하며 `click_widget`에서 사용
- 출력이 너무 크면 `depth`를 줄이거나 `ref_id`로 특정 영역만 탐색

---

#### `click_widget`

위젯을 클릭합니다. Chrome MCP의 `computer` (click)에 대응합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ref_id` | string | Yes* | `read_widget_tree`에서 받은 참조 ID |
| `coordinate` | object | Yes* | 직접 좌표 지정 `{"x": 100, "y": 200}` |
| `click_type` | string | No | `"left"`, `"right"`, `"double"` (default: "left") |
| `text` | string | No | 클릭 후 입력할 텍스트 (SEditableTextBox 용) |
| `modifiers` | string | No | `"ctrl"`, `"shift"`, `"alt"`, `"ctrl+shift"` |

*`ref_id` 또는 `coordinate` 중 하나는 필수

**Returns**:
```json
{
  "success": true,
  "widget": {
    "ref_id": "w_1",
    "type": "SButton",
    "text": "Compile"
  },
  "clicked_at": {"x": 140, "y": 62},
  "text_entered": null
}
```

**Example**:
```python
# Click Compile button by ref_id
await client.call_tool("click_widget", {"ref_id": "w_1"})

# Click and enter text (for input fields)
await client.call_tool("click_widget", {
    "ref_id": "w_10",
    "text": "800.0"
})

# Double-click a tree item
await client.call_tool("click_widget", {
    "ref_id": "w_5",
    "click_type": "double"
})

# Click by coordinate (from screenshot analysis)
await client.call_tool("click_widget", {
    "coordinate": {"x": 140, "y": 62}
})

# Ctrl+click for multi-select
await client.call_tool("click_widget", {
    "ref_id": "w_6",
    "modifiers": "ctrl"
})
```

**Safety Notes**:
- 클릭 전 위젯의 `enabled` 상태 확인 권장
- 텍스트 입력은 해당 위젯이 `SEditableTextBox` 타입일 때만 동작
- 저장/컴파일 등 중요 작업은 사용자 확인 필요 (`click_type: "left"`로 버튼 클릭)

---

### 3.7 Debug Tools

#### `read_log`

Output Log의 내용을 읽습니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pattern` | string | No | 필터 패턴 (regex) |
| `category` | string | No | 로그 카테고리 |
| `verbosity` | string | No | `"Error"`, `"Warning"`, `"Log"`, `"All"` (default: "All") |
| `limit` | number | No | 최대 라인 수 (default: 100) |
| `since_last_read` | boolean | No | 마지막 읽기 이후만 (default: false) |

**Returns**:
```json
{
  "total_lines": 1523,
  "returned_lines": 100,
  "messages": [
    {
      "timestamp": "2024-01-15 10:30:45.123",
      "category": "LogBlueprintUserMessages",
      "verbosity": "Log",
      "message": "Health changed to 50.0"
    },
    {
      "timestamp": "2024-01-15 10:30:46.456",
      "category": "LogTemp",
      "verbosity": "Warning",
      "message": "Asset not found: /Game/Missing"
    },
    {
      "timestamp": "2024-01-15 10:30:47.789",
      "category": "LogCompile",
      "verbosity": "Error",
      "message": "BP_Player: Error in node 'Set Health'"
    }
  ]
}
```

**Example**:
```python
# Get only errors
errors = await client.call_tool("read_log", {
    "verbosity": "Error",
    "limit": 50
})

# Filter by pattern
compile_logs = await client.call_tool("read_log", {
    "pattern": "Compile|Blueprint",
    "limit": 100
})
```

---

### 3.8 Media Tools

#### `capture_window`

현재 포커스된 창 또는 지정된 창의 스크린샷을 캡처합니다.

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `window_id` | string | No | 특정 창 (default: 포커스된 창) |
| `include_ui` | boolean | No | 에디터 UI 포함 (default: true) |
| `filename` | string | No | 저장 파일명 (default: auto) |

**Returns**:
```json
{
  "success": true,
  "window_id": "win_1",
  "window_title": "BP_Player",
  "image_path": "D:/Projects/MyGame/Saved/Screenshots/BP_Player_20240115_103045.png",
  "width": 1920,
  "height": 1080,
  "format": "PNG",
  "file_size": 2097152,
  "image_id": "img_001"
}
```

**Notes**:
- `image_id`는 후속 분석에 사용 가능
- Level Editor 뷰포트 캡처 시 `include_ui: false`로 순수 뷰포트만 캡처 가능

**Example**:
```python
# Capture current focused window
await client.call_tool("capture_window", {})

# Capture specific window
await client.call_tool("capture_window", {
    "window_id": "win_0",
    "include_ui": false,
    "filename": "level_viewport"
})
```

---

## 4. Protocol

### 4.1 Transport Layer

TCP Socket 연결을 사용하며, LSP와 유사한 메시지 프레이밍을 적용합니다.

**Connection Details**:
- Host: `localhost` (기본값)
- Port: `9876` (기본값)
- Encoding: `UTF-8`

### 4.2 Message Format

```
Content-Length: <byte-length>\r\n
\r\n
<JSON-RPC 2.0 message>
```

### 4.3 JSON-RPC 2.0 Messages

#### Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "editor_context",
  "params": {}
}
```

#### Response (Success)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": { ... }
}
```

#### Response (Error)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32001,
    "message": "Window not found",
    "data": { "window_id": "win_99" }
  }
}
```

### 4.4 Error Codes

| Code | Message | Description |
|------|---------|-------------|
| -32700 | Parse error | Invalid JSON |
| -32600 | Invalid Request | 잘못된 JSON-RPC 요청 |
| -32601 | Method not found | 존재하지 않는 메소드 |
| -32602 | Invalid params | 잘못된 파라미터 |
| -32603 | Internal error | 내부 서버 오류 |
| -32001 | Asset not found | 에셋을 찾을 수 없음 |
| -32002 | Window not found | 창을 찾을 수 없음 |
| -32003 | Widget not found | 위젯을 찾을 수 없음 |
| -32004 | Widget not interactive | 상호작용 불가능한 위젯 |
| -32005 | Capture failed | 스크린샷 실패 |
| -32006 | Invalid reference | 만료된 참조 ID |

### 4.5 Connection Lifecycle

```
1. MCP Server starts → TCP connection to UE Plugin (localhost:9876)
2. UE Plugin: {"jsonrpc":"2.0","method":"initialized","params":{"version":"0.1.0"}}
3. Normal operation: Request/Response
4. Heartbeat every 30s: ping/pong
5. Shutdown: {"jsonrpc":"2.0","method":"shutdown"}
```

---

## 5. Plugin Implementation Guide

### 5.1 Plugin Structure

> **구현 상태:** 실제 플러그인은 `RekahUnrealBridgeMCP`로 구현됨

```
RekahUnrealBridgeMCP/                    ← 실제 플러그인 구조
├── RekahUnrealBridgeMCP.uplugin
├── Source/
│   └── RekahUnrealBridgeMCP/
│       ├── RekahUnrealBridgeMCP.Build.cs
│       └── Public/                       ← 모든 코드 배치 (Private 미사용, YAGNI)
│           ├── RekahUnrealBridgeMCPModule.h
│           ├── RekahUnrealBridgeMCPModule.cpp
│           │
│           └── Network/                  ← ✅ Plan 02 완료
│               ├── RekahTcpMcpServer.h   ← FRunnable 기반 TCP 서버
│               ├── RekahTcpMcpServer.cpp
│               ├── RekahTcpMcpConnection.h  ← 클라이언트 연결, LSP/MCP 프로토콜
│               └── RekahTcpMcpConnection.cpp
│
│           # 추후 추가 예정 (Plan 03+)
│           # ├── JsonRpc/
│           # │   └── RekahJsonRpcHandler.h/cpp
│           # └── Commands/
│           #     └── ...
│
├── scripts/
│   └── test_tcp_connection.py            ← TCP 테스트 스크립트
├── Config/
├── Resources/
└── README.md
```

> **설계 원칙:**
> - `namespace Rekah` 사용
> - 파일명에 `Rekah` 접두사 포함
> - Private 폴더 미사용 (YAGNI 원칙)

### 5.2 Key UE APIs

#### Window/Tab Management

```cpp
// Global Tab Manager
FGlobalTabmanager::Get()

// Get all open tabs
TArray<TSharedRef<SDockTab>> OpenTabs;
FGlobalTabmanager::Get()->GetAllTabs(OpenTabs);

// Activate specific tab
FGlobalTabmanager::Get()->TryInvokeTab(TabId);

// Get currently focused window
TSharedPtr<SWindow> FocusedWindow = FSlateApplication::Get().GetActiveTopLevelWindow();
```

#### Widget Reflector Pattern

```cpp
// Get all widgets under a window
void TraverseWidgetTree(TSharedRef<SWidget> Widget, int32 Depth)
{
    // Widget type
    FString WidgetType = Widget->GetTypeAsString();

    // Widget geometry
    FGeometry Geometry = Widget->GetCachedGeometry();
    FVector2D Position = Geometry.GetAbsolutePosition();
    FVector2D Size = Geometry.GetAbsoluteSize();

    // Widget text (if any)
    FText WidgetText;
    if (TSharedPtr<STextBlock> TextBlock = StaticCastSharedRef<STextBlock>(Widget))
    {
        WidgetText = TextBlock->GetText();
    }

    // Traverse children
    FChildren* Children = Widget->GetChildren();
    for (int32 i = 0; i < Children->Num(); i++)
    {
        TraverseWidgetTree(Children->GetChildAt(i), Depth + 1);
    }
}

// Start from top-level window
TSharedPtr<SWindow> Window = FSlateApplication::Get().GetActiveTopLevelWindow();
if (Window)
{
    TraverseWidgetTree(Window.ToSharedRef(), 0);
}
```

#### Widget Interaction

```cpp
// Simulate click on widget
void ClickWidget(TSharedRef<SWidget> Widget, EKeys::Type Button = EKeys::LeftMouseButton)
{
    FGeometry Geometry = Widget->GetCachedGeometry();
    FVector2D Center = Geometry.GetAbsolutePositionAtCoordinates(FVector2D(0.5f, 0.5f));

    FPointerEvent ClickEvent(
        0,
        Center,
        Center,
        TSet<FKey>(),
        Button,
        0,
        FModifierKeysState()
    );

    FSlateApplication::Get().ProcessMouseButtonDownEvent(nullptr, ClickEvent);
    FSlateApplication::Get().ProcessMouseButtonUpEvent(ClickEvent);
}

// Enter text in editable text box
void EnterText(TSharedRef<SEditableTextBox> TextBox, const FString& Text)
{
    TextBox->SetText(FText::FromString(Text));
}
```

#### Asset Registry

```cpp
// Search assets
IAssetRegistry& AssetRegistry = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry").Get();

FARFilter Filter;
Filter.ClassNames.Add(TEXT("Blueprint"));
Filter.PackagePaths.Add(TEXT("/Game/Blueprints"));
Filter.bRecursivePaths = true;

TArray<FAssetData> Assets;
AssetRegistry.GetAssets(Filter, Assets);

for (const FAssetData& Asset : Assets)
{
    FString AssetName = Asset.AssetName.ToString();
    FString AssetPath = Asset.PackageName.ToString();
}
```

#### Screenshot Capture

```cpp
// Capture window
bool CaptureWindow(TSharedRef<SWindow> Window, const FString& FilePath)
{
    FWidgetRenderer Renderer(true);

    TSharedRef<SWidget> WindowContent = Window->GetContent().ToSharedRef();
    FVector2D Size = WindowContent->GetCachedGeometry().GetAbsoluteSize();

    TSharedRef<FSlateRenderer> SlateRenderer = FSlateApplication::Get().GetRenderer();
    TArray<FColor> Bitmap;

    // Render to bitmap
    SlateRenderer->DrawWindowAndChildren(Window, Bitmap);

    // Save to file
    IImageWrapperModule& ImageModule = FModuleManager::LoadModuleChecked<IImageWrapperModule>("ImageWrapper");
    TSharedPtr<IImageWrapper> ImageWrapper = ImageModule.CreateImageWrapper(EImageFormat::PNG);
    ImageWrapper->SetRaw(Bitmap.GetData(), Bitmap.Num() * sizeof(FColor), Size.X, Size.Y, ERGBFormat::BGRA, 8);

    return FFileHelper::SaveArrayToFile(ImageWrapper->GetCompressed(100), *FilePath);
}
```

### 5.3 Thread Safety

모든 Slate/에디터 API 호출은 GameThread에서 실행해야 합니다.

```cpp
AsyncTask(ENamedThreads::GameThread, [this]()
{
    // Safe to call Slate/Editor APIs here
    TSharedPtr<SWindow> Window = FSlateApplication::Get().GetActiveTopLevelWindow();
});
```

---

## Appendix A: Chrome MCP Mapping

| Chrome MCP | Unreal Bridge | Notes |
|------------|---------------|-------|
| `tabs_context_mcp` | `editor_context` | 열린 창/탭 목록, 포커스 정보 |
| `navigate` | `focus_window` | 창/탭 전환 |
| `read_page` | `read_widget_tree` | DOM → Widget Tree |
| `get_page_text` | `read_details_panel` | Details Panel 속성 |
| `find` | `find_assets` | Content Browser 검색 |
| `computer` (click) | `click_widget` | 위젯 클릭 |
| `computer` (screenshot) | `capture_window` | 창 캡처 |
| `read_console_messages` | `read_log` | Output Log |

---

## Appendix B: Future Considerations (Phase 2)

- `type_text` - 키보드 입력 시뮬레이션
- `drag_widget` - 드래그 앤 드롭
- `read_viewport` - 3D 뷰포트 객체 정보
- `execute_command` - 콘솔 명령 실행
- Blueprint 노드 그래프 읽기/수정
- 액터 스폰/삭제
