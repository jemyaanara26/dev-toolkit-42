import sys
import datetime
from typing import Any

class DevLogger:
    def __init__(self, prefix: str = "[dev-toolkit-42]"):
        self.prefix = prefix
        self.stream = sys.stdout

    def __call__(self, *args: Any, level: str = "INFO") -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = " ".join(map(str, args))
        output = f"{timestamp} {self.prefix} {level}: {message}"
        self.stream.write(output + "\n")
        self.stream.flush()

    def success(self, *args: Any) -> None:
        self(*args, level="SUCCESS")

    def error(self, *args: Any) -> None:
        self(*args, level="CRITICAL")

class LoggerInstance:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = DevLogger()
        return cls._instance

logger = LoggerInstance()