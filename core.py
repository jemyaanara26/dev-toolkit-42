import functools
import time
import uuid
from typing import Callable, Any

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def generate_short_id(length: int = 8) -> str:
    return uuid.uuid4().hex[:length]

def batch_process(items: list, size: int):
    return [items[i:i + size] for i in range(0, len(items), size)]

def memoize_with_expiry(ttl: int):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                val, timestamp = cache[args]
                if now - timestamp < ttl:
                    return val
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator