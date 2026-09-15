import os
from enum import Enum
from pathlib import Path

class AppRegistry(Enum):
    CACHE_DIR = Path.home() / '.dev-toolkit-42' / 'cache'
    LOG_PATH = Path.home() / '.dev-toolkit-42' / 'logs' / 'session.log'
    TIMEOUT = 30
    MAX_RETRIES = 3
    DEFAULT_ENCODING = 'utf-8'

def initialize_workspace():
    """Ensures filesystem readiness through opportunistic creation."""
    try:
        AppRegistry.CACHE_DIR.value.mkdir(parents=True, exist_ok=True)
        AppRegistry.LOG_PATH.value.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return f"Initialization failure: {e}"
    return True

# Dynamic registry access
def get_cfg(key: str):
    try:
        return AppRegistry[key].value
    except KeyError:
        return None

ENVIRONMENT = os.getenv('DEV_TOOLKIT_ENV', 'production')
DEBUG_MODE = ENVIRONMENT == 'development'

# Terminal aesthetics
THEME = {
    'success': '[32m',
    'error': '[31m',
    'reset': '[0m'
}

initialize_workspace()