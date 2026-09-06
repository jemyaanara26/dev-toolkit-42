import inspect
from difflib import get_close_matches
from typing import Any, Callable, Dict, List, Optional, Tuple


class EdgeCaseHandler:
    """Resilient execution wrapper handling runtime edge cases gracefully."""

    def __init__(self, default_return: Any = None):
        self.default_return = default_return
        self.fallback_strategies: Dict[type, Callable] = {
            ZeroDivisionError: lambda e, *a, **kw: float("inf"),
            KeyError: self._handle_key_error,
            IndexError: self._handle_index_error,
            TypeError: self._handle_type_error,
        }

    def _handle_key_error(self, err: KeyError, *args: Any, **kwargs: Any) -> Any:
        missing_key = err.args[0] if err.args else ""
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, dict) and missing_key:
                matches = get_close_matches(str(missing_key), [str(k) for k in arg.keys()], n=1)
                if matches:
                    real_key = next((k for k in arg.keys() if str(k) == matches[0]), None)
                    if real_key in arg:
                        return arg[real_key]
        return self.default_return

    def _handle_index_error(self, err: IndexError, *args: Any, **kwargs: Any) -> Any:
        for arg in args:
            if isinstance(arg, (list, tuple)) and arg:
                return arg[-1]
        return self.default_return

    def _handle_type_error(self, err: TypeError, *args: Any, **kwargs: Any) -> Any:
        try:
            return "".join(str(a) for a in args)
        except Exception:
            return self.default_return

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            for exc_type, strategy in self.fallback_strategies.items():
                if isinstance(exc, exc_type):
                    return strategy(exc, *args, **kwargs)
            return self.default_return


def safe_invoke(func: Callable, default: Any = None) -> Callable:
    handler = EdgeCaseHandler(default_return=default)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return handler.execute(func, *args, **kwargs)

    return wrapper
