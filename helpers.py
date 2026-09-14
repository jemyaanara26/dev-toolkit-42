import json
import functools
from typing import Callable, Any

def pipe(value: Any, *funcs: Callable) -> Any:
    return functools.reduce(lambda v, f: f(v), funcs, value)

def memoize_file(filepath: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = {}
        try:
            with open(filepath, 'r') as f:
                cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
                with open(filepath, 'w') as f:
                    json.dump(cache, f)
            return cache[key]
        return wrapper
    return decorator

def retry(attempts: int = 3) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator

def flatten(lst: list) -> list:
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, list) else [sublist])]