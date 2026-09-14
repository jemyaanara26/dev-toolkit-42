import time
import random
from typing import Iterator, Type, Tuple

class RetryAttempt:
    def __init__(self, manager):
        self.manager = manager

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.manager.success = True
            return True
        if issubclass(exc_type, self.manager.exceptions):
            if self.manager.attempts >= self.manager.max_attempts:
                return False
            return True
        return False

class ResilientProcessor:
    def __init__(self, max_attempts: int = 3, backoff: float = 1.5, exceptions: Tuple[Type[BaseException], ...] = (Exception,)):
        self.max_attempts = max_attempts
        self.backoff = backoff
        self.exceptions = exceptions
        self.attempts = 0
        self.success = False

    def __iter__(self) -> Iterator[RetryAttempt]:
        delay = 0.5
        while self.attempts < self.max_attempts and not self.success:
            self.attempts += 1
            yield RetryAttempt(self)
            if self.success:
                break
            if self.attempts < self.max_attempts:
                time.sleep(delay * (0.5 + random.random()))
                delay *= self.backoff