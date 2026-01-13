---
name: python-coding
description: Python/UV 기반 코드 작성 가이드라인
---

# Python 코드 작성 가이드라인

## 기본 원칙
- 구현은 작게/간단하게
- 오버 엔지니어링 금지
- 특별한 요청이 없는 이상, 예외처리 과도하게 하지 않기
- 주석은 항상 영문으로
- 주석의 첫단어 시작은 대문자가 아닌 소문자로 일관성 있게!

## 파일 구조
- python은 기본적으로 uv 기반이며, 때에 따라 hatch 기반일 수 있음
- 파일명: `{이름}_utils.py`
- 함수 구현: `{이름}_utils.py`

## 테스트 코드
- 위치: `./tests/test_{파일이름}.py`
- 함수 단위로 구현
- pytest 기반이 아닌 native 구현
- 임시 파일/디렉토리는 `./intermediates/` 하위에 생성
- `tempfile.mkdtemp()` 사용 금지 (프로젝트 외부 경로 문제)

## 상태 관리
- context 기반 코딩
- singleton 패턴 사용: `singleton_utils.py` 참고
- 프로젝트에 없다면 [REFERENCE.md](./REFERENCE.md) 참고하여 구현 권장

## 로깅
- `logging_utils.py`에 구현된 것 참고
- 프로젝트에 없다면 [REFERENCE.md](./REFERENCE.md) 참고하여 구현 권장

## 보안 설정
- 민감 정보는 VCS에 올라가지 않도록 config로 관리
- `config_utils.py` 참고
- 프로젝트에 없다면 [REFERENCE.md](./REFERENCE.md) 참고하여 구현 권장
