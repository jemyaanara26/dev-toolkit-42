import functools
from typing import Any, Callable, Mapping

class DeepAccess:
    """Dynamic key/attribute access helper supporting dot and index syntax."""
    def __init__(self, path: str):
        self._parts = [p.strip("]") for p in path.replace("[", ".").split(".") if p]

    def __call__(self, target: Any) -> Any:
        current = target
        for part in self._parts:
            try:
                if part.isdigit() and not hasattr(current, part):
                    current = current[int(part)]
                elif isinstance(current, Mapping) and part in current:
                    current = current[part]
                else:
                    current = getattr(current, part)
            except (KeyError, IndexError, AttributeError, TypeError):
                return None
        return current

class Pipeline:
    """Fluent function execution pipeline using left-shift overloading."""
    def __init__(self, data: Any):
        self.data = data

    def __lshift__(self, action: Callable[[Any], Any]) -> "Pipeline":
        return Pipeline(action(self.data))

    def unwrap(self) -> Any:
        return self.data

def safe_bind(position: int, *args, **kwargs) -> Callable:
    """Binds arguments starting at a specific positional slot dynamically."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*runtime_args, **runtime_kwargs):
            merged_args = list(runtime_args)
            for i, arg in enumerate(args):
                merged_args.insert(position + i, arg)
            return func(*merged_args, **{**kwargs, **runtime_kwargs})
        return wrapper
    return decorator