import functools
from typing import Any, Callable, Dict

class ValidationError(Exception):
    pass

def validate_input(schema: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, expected_type in schema.items():
                value = kwargs.get(key)
                if value is None:
                    raise ValidationError(f"missing required param: {key}")
                if not isinstance(value, expected_type):
                    raise ValidationError(f"type mismatch for {key}: expected {expected_type.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_input({"data": dict, "priority": int})
def process_payload(**kwargs):
    return f"processing {kwargs['data']} at level {kwargs['priority']}"

def run_loop(items):
    for item in items:
        try:
            result = process_payload(**item)
            print(f"Success: {result}")
        except (ValidationError, TypeError) as e:
            print(f"Validation failure: {e}")

if __name__ == "__main__":
    data_stream = [
        {"data": {"task": "a"}, "priority": 1},
        {"data": "bad_input", "priority": 2},
        {"data": {"task": "b"}, "priority": "high"}
    ]
    run_loop(data_stream)