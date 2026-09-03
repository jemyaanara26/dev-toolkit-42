[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# dev-toolkit-42

`dev-toolkit-42` is a curated collection of utility modules designed to streamline common Python development workflows. It eliminates repetitive boilerplate by providing robust helpers for logging configuration, environment variable parsing, and execution profiling out of the box.

## Features

- **Structured Logger:** Pre-configured JSON logging with colorized console outputs for development and structured formats for production.
- **Smart Env Loader:** Type-safe environment variable casting with automatic validation and fallback defaults.
- **Performance Timer:** A lightweight decorator and context manager to benchmark critical code blocks with microsecond precision.

## Installation

Install the package directly from PyPI:

```bash
pip install dev-toolkit-42
```

## Quick Start

```python
from dev_toolkit_42 import Logger, env, profile

# 1. Initialize structured logging
logger = Logger(service_name="api-server")

# 2. Retrieve type-safe environment variables
DEBUG_MODE = env.get_bool("DEBUG", default=False)
PORT = env.get_int("PORT", default=8080)

# 3. Profile execution time with decorators
@profile
def fetch_system_metrics():
    logger.info("Retrieving system status...", extra={"port": PORT, "debug": DEBUG_MODE})
    # Simulated workload
    return {"status": "healthy"}

if __name__ == "__main__":
    fetch_system_metrics()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.