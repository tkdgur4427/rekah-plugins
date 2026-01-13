# 레퍼런스 구현 가이드

프로젝트에 해당 파일이 없으면 아래 패턴으로 구현 권장.

## singleton_utils.py

싱글톤 패턴 베이스 클래스.

```python
class SingletonInstance:
    """base class for singleton pattern implementation"""

    __instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        """create or get the singleton instance"""
        if cls.__instance is None:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    @classmethod
    def reset_instance(cls):
        """reset the singleton instance (for testing)"""
        cls.__instance = None
```

**사용 예시:**
```python
class MyService(SingletonInstance):
    def __init__(self, config):
        self.config = config

# 첫 호출 시 인스턴스 생성
service = MyService.instance(config={"key": "value"})

# 이후 호출은 동일 인스턴스 반환
same_service = MyService.instance()
```

## logging_utils.py

rich 기반 싱글톤 로거.

```python
from singleton_utils import SingletonInstance

class Logger(SingletonInstance):
    """singleton logger class with rich support"""

    def __init__(self, prefix: str = "", log_dir: str = "./logs"):
        self.prefix = prefix
        self.log_dir = log_dir
        # logging 설정 초기화...

    def info(self, message: str):
        """log info level message"""
        pass

    def error(self, message: str):
        """log error level message"""
        pass

    def warning(self, message: str):
        """log warning level message"""
        pass
```

**데코레이터:**
```python
def logging_func(desc: str = ""):
    """decorator for function logging"""
    def decorator(function):
        def wrapper(*args, **kwargs):
            Logger.instance().info(f"[start] {function.__name__}")
            result = function(*args, **kwargs)
            Logger.instance().info(f"[end] {function.__name__}")
            return result
        return wrapper
    return decorator
```

**사용 예시:**
```python
@logging_func("processing data")
def process_data():
    pass

Logger.instance().info("hello")
```

## config_utils.py

config.ini 기반 설정 관리.

```python
import configparser

global_config = configparser.ConfigParser()

def load_config_ini() -> None:
    """load configuration file"""
    config_path = "./config.ini"
    if os.path.exists(config_path):
        global_config.read(config_path, encoding="utf-8")

def get_config_value(section: str, key: str, default=None):
    """get configuration value"""
    try:
        return global_config.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default

# 모듈 import 시 자동 로드
load_config_ini()
```

**config.ini 예시:**
```ini
[database]
host = localhost
port = 5432

[api]
key = your_api_key_here
```

**사용 예시:**
```python
db_host = get_config_value("database", "host", default="localhost")
```
