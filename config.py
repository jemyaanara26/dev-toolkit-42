"""Configuration management with dynamic environment parsing."""

import os
from typing import Any, Dict, Optional


class AppConfig:
    """Holder for application settings loaded from the environment."""

    def __init__(self, prefix: str = "DT42_") -> None:
        """Initialize configuration using a specific environment variable prefix."""
        self._prefix: str = prefix
        self._cache: Dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value with an optional fallback."""
        env_key = f"{self._prefix}{key.upper()}"
        if env_key in self._cache:
            return self._cache[env_key]
        
        val = os.getenv(env_key, default)
        self._cache[env_key] = self._coercion(val)
        return self._cache[env_key]

    def _coercion(self, val: Any) -> Any:
        """Magically coerce string environment variables into proper types."""
        if not isinstance(val, str):
            return val
        
        lowered = val.lower()
        if lowered in ("true", "yes", "1", "on"):
            return True
        if lowered in ("false", "no", "0", "off"):
            return False
        
        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            return val

    def dump(self) -> Dict[str, Any]:
        """Return a dictionary representation of all cached configurations."""
        return dict(self._cache)


active_config: AppConfig = AppConfig()
