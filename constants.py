import sys
import functools
from typing import Any, Callable

class ConstantCache:
    """High-performance immutable constant storage with lazy resolution."""
    _registry = {}

    def __init__(self, key: str, resolver: Callable[[], Any]):
        self.key = key
        self.resolver = resolver

    def __get__(self, instance, owner) -> Any:
        if self.key not in self._registry:
            self._registry[self.key] = self.resolver()
        return self._registry[self.key]

def _load_system_metrics():
    return {'cpu_threads': sys.maxsize, 'python_version': sys.version_info[:3]}

class SystemConfig:
    """
    Optimized global settings using descriptor-based lazy evaluation
    to prevent unnecessary runtime overhead during module initialization.
    """
    MAX_RETRY_ATTEMPTS = 5
    BUFFER_SIZE = 4096 * 8
    SYSTEM_METRICS = ConstantCache('metrics', _load_system_metrics)
    TIMEOUT_SEC = 30.5

# Expose as singleton-like interface
CONFIG = SystemConfig()

if __name__ == '__main__':
    print(f"Initial Config: {CONFIG.BUFFER_SIZE}")
    print(f"Lazy Metrics: {CONFIG.SYSTEM_METRICS}")