import os
from collections import ChainMap
from typing import Any, Dict

class SelfInterpolatingConfig:
    """Dynamic configuration loader with chain-resolution, environmental overrides, and string interpolation."""

    def __init__(self, defaults: Dict[str, Any], filepath: str | None = None):
        self._defaults = defaults
        self._file_data: Dict[str, Any] = {}
        if filepath and os.path.exists(filepath):
            with open(filepath, "r") as f:
                for line in f:
                    clean = line.strip()
                    if "=" in clean and not clean.startswith("#"):
                        k, v = clean.split("=", 1)
                        self._file_data[k.strip()] = v.strip()

        # Resolving hierarchy: environment -> configuration file -> default parameters
        self._store = ChainMap(os.environ, self._file_data, self._defaults)
        self._resolving: set[str] = set()

    def __getattr__(self, name: str) -> Any:
        if name not in self._store:
            raise AttributeError(f"Configuration parameter '{name}' is not defined")
        return self._interpolate(name, self._store[name])

    def _interpolate(self, key: str, value: Any) -> Any:
        if not isinstance(value, str) or "${" not in value:
            return value

        if key in self._resolving:
            raise ValueError(f"Circular dependency detected during interpolation of: {key}")

        self._resolving.add(key)
        try:
            while "${" in value:
                start = value.find("${")
                end = value.find("}", start)
                if end == -1:
                    break
                var_name = value[start + 2:end]
                resolved_val = str(getattr(self, var_name))
                value = value[:start] + resolved_val + value[end + 1:]
            return value
        finally:
            self._resolving.remove(key)

    def to_dict(self) -> Dict[str, Any]:
        """Extract all keys and dynamically resolve references in a complete dictionary export."""
        return {k: getattr(self, k) for k in self._store.keys()}
