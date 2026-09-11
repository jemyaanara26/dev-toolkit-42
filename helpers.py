from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
import functools

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Functional pipeline builder for arbitrary callables."""
    def pipeline(data: Any) -> Any:
        return functools.reduce(lambda v, f: f(v), functions, data)
    return pipeline

def chunk_iterable(items: List[T], size: int) -> List[List[T]]:
    """Split list into n-sized chunks using slice notation."""
    if size <= 0:
        return [items]
    return [items[i:i + size] for i in range(0, len(items), size)]

def deep_get(data: Dict[str, Any], path: str, default: Optional[Any] = None) -> Any:
    """Dot-notation navigation through nested dictionaries."""
    keys: List[str] = path.split('.')
    current: Any = data
    try:
        for key in keys:
            current = current[key]
        return current if current is not None else default
    except (KeyError, TypeError):
        return default

def retry(attempts: int = 3) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for simple function execution repetition."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_ex: Exception = Exception()
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator