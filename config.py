import json
import os
from typing import Any, Dict

class ConfigLoader:
    """A magical recursive dictionary merger for configuration hell."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_data = json.load(f)
                self._merge(self._data, user_data)

    def _merge(self, base: Dict, overrides: Dict) -> None:
        for key, value in overrides.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self._data
        try:
            for k in keys:
                val = val[k]
            return val
        except (KeyError, TypeError):
            return default

def load_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load(path)
    return loader