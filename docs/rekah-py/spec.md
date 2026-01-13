# rekah-py 플러그인 명세서

## 개요

Python/UV 기반 개발을 위한 Claude Code 플러그인입니다.
`D:\rekah_web_server\plugins\rekah-dev-plugin\skills\python-coding`의 가이드라인을 기반으로 합니다.

## 플러그인 구조

```
plugins/rekah-py/
├── .claude-plugin/
│   └── plugin.json          # 플러그인 매니페스트
└── skills/
    └── python-coding/
        ├── SKILL.md         # Python 코딩 가이드라인
        └── REFERENCE.md     # 레퍼런스 소스코드 (singleton, logging, config)
```

## 구현 상세

### 1. plugin.json

```json
{
  "name": "rekah-py",
  "version": "0.1.0",
  "description": "Python/UV 기반 개발을 위한 Claude Code 플러그인",
  "author": {
    "name": "Haker"
  },
  "repository": "https://github.com/tkdgur4427/rekah-plugins"
}
```

- MCP 서버: 없음 (순수 스킬 기반 플러그인)
- 훅: 없음

### 2. python-coding 스킬

**SKILL.md 내용:**

```yaml
---
name: python-coding
description: Python/UV 기반 코드 작성 가이드라인
---
```

**가이드라인 항목:**

| 항목 | 규칙 |
|------|------|
| 기본 원칙 | 작은 구현, 오버 엔지니어링 금지, 최소한의 예외처리 |
| 주석 | 영문, 소문자 시작 |
| 파일 구조 | UV 기반, `{이름}_utils.py` 형식 |
| 테스트 | `./tests/test_{파일이름}.py`, native 구현 (pytest 아님) |
| 임시 파일 | `./intermediates/` 하위에 생성 |
| 상태 관리 | context 기반, singleton 패턴 → [REFERENCE.md](./REFERENCE.md) 참조 |
| 로깅 | [REFERENCE.md](./REFERENCE.md) 참조 |
| 보안 | 민감 정보는 config로 관리 → [REFERENCE.md](./REFERENCE.md) 참조 |

### 3. REFERENCE.md (레퍼런스 가이드)

프로젝트에 해당 파일이 없으면 아래 패턴으로 구현 권장:

#### singleton_utils.py
- `SingletonInstance` 베이스 클래스
- `instance()` - 싱글톤 인스턴스 반환
- `reset_instance()` - 테스트용 리셋

#### logging_utils.py
- `Logger` - rich 기반 싱글톤 로거
- `@logging_func` - 함수 로깅 데코레이터

#### config_utils.py
- `load_config_ini()` - config.ini 로드
- `get_config_value(section, key)` - 설정값 조회

## 구현 순서

1. `plugins/rekah-py/.claude-plugin/plugin.json` 생성
2. `plugins/rekah-py/skills/python-coding/SKILL.md` 생성
3. `plugins/rekah-py/skills/python-coding/REFERENCE.md` 생성
4. 테스트: 새 세션에서 플러그인 로드 확인

## 확장 계획

추가 스킬 후보:
- (추후 필요 시 추가)
