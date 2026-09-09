import functools
import logging
import time
from typing import Callable, Any

def resilient_wrapper(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, ValueError) as e:
                    last_ex = e
                    logging.warning(f'attempt {attempt+1} failed: {e}')
                    time.sleep(delay * (2 ** attempt))
                except Exception as e:
                    logging.critical(f'fatal non-recoverable error: {e}')
                    raise e
            raise last_ex or RuntimeError('unknown failure')
        return wrapper
    return decorator

def safe_dict_get(data: dict, path: str, default: Any = None) -> Any:
    keys = path.split('.')
    curr = data
    try:
        for key in keys:
            curr = curr[key]
        return curr if curr is not None else default
    except (KeyError, TypeError, AttributeError):
        return default

def suppress_errors(default_val: Any = None):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_val
        return wrapper
    return decorator