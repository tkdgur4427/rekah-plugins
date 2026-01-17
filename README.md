# Rekah Plugins

Rekah 개발 도구 플러그인 마켓플레이스

## 설치

```bash
# 만약, claude code 실행 중이라면, 'claude plugin' 대신 '/plugin'
# 마켓플레이스 추가
claude plugin marketplace add tkdgur4427/rekah-plugins

# 플러그인 설치
# 1. unreal engine
claude plugin install rekah-unreal@rekah-plugins --scope project
# 2. python 
claude plugin install rekah-py@rekah-plugins --scope project
```

## 플러그인 목록

### rekah-unreal

Unreal Engine 개발을 위한 Claude Code 플러그인

**기능:**
- `/rekah-unreal:build` - Unreal 프로젝트 빌드
- `unreal-cpp-patterns` skill - C++ 코딩 표준 가이드

**MCP 서버:**
- `rekah-unreal` - [rekah-unreal-mcp](https://github.com/tkdgur4427/rekah-unreal-mcp)

## 라이선스

MIT
