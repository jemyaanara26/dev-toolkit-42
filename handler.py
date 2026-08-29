import time
from functools import reduce, wraps
from typing import Any, Callable, Dict, List

def safe_divide(numerator: float, denominator: float, fallback: float = 0.0) -> float:
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return fallback

def flatten_nested(data: List[Any]) -> List[Any]:
    result = []
    for item in data:
        if isinstance(item, list):
            result.extend(flatten_nested(item))
        else:
            result.append(item)
    return result

def create_retry_wrapper(max_attempts: int = 3, base_delay: float = 0.5) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(base_delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

def batch_data(items: List[Any], size: int = 10) -> List[List[Any]]:
    if not isinstance(items, list):
        return [items]
    return [items[i:i + size] for i in range(0, len(items), size)]

def merge_collections(*collections: Dict[str, Any]) -> Dict[str, Any]:
    return reduce(lambda acc, d: {**acc, **d}, collections, {})

def handle_common(data: Any, op_type: str) -> Any:
    operations = {
        "divide": lambda x: safe_divide(x[0], x[1]) if isinstance(x, (list, tuple)) and len(x) >= 2 else x,
        "flatten": flatten_nested,
        "batch": batch_data,
        "merge": lambda x: merge_collections(*x) if isinstance(x, (list, tuple)) else x
    }
    if op_type in operations:
        func = operations[op_type]
        if op_type in ["batch", "divide"]:
            return func(data)
        return func(data)
    return data

if __name__ == "__main__":
    sample = [1, [2, [3, 4]], 5]
    print("Flattened:", handle_common(sample, "flatten"))
    print("Batched:", handle_common([10,20,30,40,50,60], "batch"))
    print("Merged:", handle_common([{"a":1}, {"b":2}], "merge"))
    print("Divided:", handle_common((10, 2), "divide"))