import time
import collections
from typing import Callable, Any

class AdaptiveExecutor:
    """
    An unusual performance optimizer that measures execution times in real-time
    and adaptively decides whether to use caching or raw inline execution.
    """
    def __init__(self, threshold_ms: float = 5.0, history_size: int = 20):
        self.threshold_ns = threshold_ms * 1_000_000
        self.history = collections.deque(maxlen=history_size)
        self.cache = {}
        self.avg_duration = 0.0

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(kwargs.items()))
            
            if self.avg_duration < self.threshold_ns and self.history:
                start = time.perf_counter_ns()
                result = func(*args, **kwargs)
                duration = time.perf_counter_ns() - start
                self.history.append(duration)
                self.avg_duration = sum(self.history) / len(self.history)
                return result

            if key in self.cache:
                return self.cache[key]

            start = time.perf_counter_ns()
            result = func(*args, **kwargs)
            duration = time.perf_counter_ns() - start

            self.history.append(duration)
            self.avg_duration = sum(self.history) / len(self.history)
            self.cache[key] = result
            return result

        return wrapper