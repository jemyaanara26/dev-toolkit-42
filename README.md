# dev-toolkit-42

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`dev-toolkit-42` is a versatile suite of command-line utilities and helper functions designed to streamline daily Python development workflows. It automates tedious tasks like configuration validation, environment auditing, and multi-format logging with a single, unified interface.

## Features

* **Auto-Environment Audit**: Scans and compares your `.env` files against `.env.example` templates to flag missing or misconfigured keys.
* **Smart Configuration Converter**: Instantly transforms configurations between YAML, JSON, and TOML with automatic schema-validation.
* **Execution Profiler**: A high-precision decorator that benchmarks Python function runtime and automatically saves execution logs to a local SQLite database.

## Installation

Install the package directly from PyPI:

```bash
pip install dev-toolkit-42
```

Or install the development version from source:

```bash
git clone https://github.com/developer/dev-toolkit-42.git
cd dev-toolkit-42
pip install -e .
```

## Quick Start

### 1. Audit Environment Variables

Verify that your local environment is correctly configured before starting your application:

```python
from dev_toolkit_42 import audit_env

# Flags keys present in .env.example but missing in .env
missing = audit_env(".env", ".env.example")
if missing:
    print(f"Warning: Missing keys found: {missing}")
```

### 2. Profile Code Execution

Benchmark critical paths in your application with database logging:

```python
import time
from dev_toolkit_42 import benchmark

@benchmark(db_log=True)
def heavy_calculation():
    time.sleep(0.5)
    return sum(i * i for i in range(100000))

# Executes and saves metrics (timestamp, duration, function name) to dev_metrics.db
heavy_calculation()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.