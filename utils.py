import time
import random
import functools
from typing import Callable, TypeVar, Any, Sequence, Type

T = TypeVar('T')

def retry_with_jitter(
    max_retries: int = 4,
    base_delay: float = 0.2,
    max_delay: float = 5.0,
    retry_exceptions: Sequence[Type[BaseException]] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator providing exponential backoff with randomized jitter using a generator pipeline."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            def schedule():
                delay = base_delay
                for attempt in range(1, max_retries + 1):
                    jittered = min(max_delay, delay * (1.0 + random.random()))
                    yield attempt, jittered
                    delay *= 2.0

            last_err: Exception | None = None
            for attempt, delay in schedule():
                try:
                    return func(*args, **kwargs)
                except retry_exceptions as err:
                    last_err = err
                    if attempt < max_retries:
                        time.sleep(delay)
            if last_err:
                raise last_err
            raise RuntimeError("Execution failed without exception")
        return wrapper
    return decorator
