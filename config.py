import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults

    def load(self, filepath: str) -> 'ConfigLoader':
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                try:
                    self._data.update(json.load(f))
                except json.JSONDecodeError:
                    pass
        return self

    def env_override(self, prefix: str = 'APP_') -> 'ConfigLoader':
        for key in self._data:
            env_val = os.getenv(f"{prefix}{key.upper()}")
            if env_val is not None:
                self._data[key] = type(self._data[key])(env_val)
        return self

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    def __getitem__(self, name: str) -> Any:
        return self._data[name]

def get_config(defaults: Dict[str, Any], path: str = 'config.json') -> ConfigLoader:
    return ConfigLoader(defaults).load(path).env_override()