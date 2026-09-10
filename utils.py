from typing import Any, Callable, Dict, List, TypeVar, Union
import functools

T = TypeVar('T')

def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """chaining of callables into a single execution pipe"""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def memoize_with_expiry(func: Callable[..., T]) -> Callable[..., T]:
    """decorator for caching with an ephemeral memory structure"""
    cache: Dict[str, T] = {}
    
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key: str = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def deep_flatten(items: List[Any]) -> List[Any]:
    """recursive flattening of nested list structures"""
    result: List[Any] = []
    for item in items:
        if isinstance(item, list):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def extract_by_key(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """selective dictionary filtering using key mapping"""
    return {k: v for k, v in data.items() if k in keys}

class Pipeline:
    """functional pipeline execution engine"""
    def __init__(self, *funcs: Callable[[Any], Any]) -> None:
        self.pipeline: Callable[[Any], Any] = compose(*funcs)

    def run(self, value: Any) -> Any:
        return self.pipeline(value)