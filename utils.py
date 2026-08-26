import os
import json
import time
import functools
from collections import defaultdict
from typing import Any, Dict, List, Callable, Optional

def timer(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Executed {func.__name__} in {elapsed:.4f} seconds")
        return result
    return wrapper

def flatten_nested(data: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    def _flatten(obj: Any, parent: str = "") -> Dict[str, Any]:
        items: Dict[str, Any] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent}{sep}{k}" if parent else k
                items.update(_flatten(v, new_key))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{parent}{sep}{i}" if parent else str(i)
                items.update(_flatten(v, new_key))
        else:
            items[parent] = obj
        return items
    return _flatten(data)

@timer
def load_and_flatten_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return flatten_nested(data)

def reorganize_by_key(items: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        group_key = item.get(key, "unknown")
        grouped[group_key].append(item)
    return dict(grouped)

def compute_project_stats(directory: str) -> Dict[str, Any]:
    py_files = []
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                py_files.append(full_path)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    total_lines += sum(1 for line in f if line.strip())
    return {
        "python_files": len(py_files),
        "total_lines": total_lines,
        "avg_lines_per_file": total_lines / len(py_files) if py_files else 0
    }

if __name__ == "__main__":
    print("Utils module loaded successfully")
    sample_data = {"a": {"b": 1, "c": [2, 3]}, "d": 4}
    print(flatten_nested(sample_data))
    stats = compute_project_stats(".")
    print(stats)