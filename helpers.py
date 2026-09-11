import time
import functools
import random
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * random.uniform(0.5, 1.5))
            raise last_ex
        return wrapper
    return decorator

def memoize_with_ttl(ttl: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                val, ts = cache[args]
                if now - ts < ttl:
                    return val
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def flatten_nested_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)