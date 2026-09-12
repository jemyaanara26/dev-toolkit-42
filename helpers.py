import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('dev-toolkit-42')

class ResilienceToolkit:
    """A whimsical decorator suite for handling the unhandleable."""
    @staticmethod
    def gracefully_fail(fallback: Any) -> Callable:
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, ZeroDivisionError) as e:
                    logger.warning(f"Edge case hit in {func.__name__}: {e}. Returning fallback.")
                    return fallback() if callable(fallback) else fallback
                except Exception as e:
                    logger.critical(f"Unforeseen collapse in {func.__name__}: {e}")
                    raise
            return wrapper
        return decorator

def safe_divide(a: float, b: float) -> float:
    """Division that smiles at zero."""
    return a / b

@ResilienceToolkit.gracefully_fail(fallback=0.0)
def robust_math(a: Any, b: Any) -> float:
    """Perform division with a safety net for bad types."""
    return safe_divide(float(a), float(b))

def sanitize_input(data: Any) -> str:
    """Force data into submission."""
    try:
        return str(data).strip()
    except Exception:
        return "null"