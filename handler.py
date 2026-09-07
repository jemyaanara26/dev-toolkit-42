import sys
import traceback
import functools

class ResilienceShield:
    def __init__(self, fallback=None, retries=3):
        self.fallback = fallback
        self.retries = retries

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError) as e:
                    print(f'Logic error: {e}')
                    return self.fallback
                except Exception as e:
                    attempts += 1
                    if attempts >= self.retries:
                        print(f'Critical failure: {traceback.format_exc()}')
                        return self.fallback
                    print(f'Retrying operation {attempts}/{self.retries}')
            return self.fallback
        return wrapper

@ResilienceShield(fallback=None, retries=2)
def secure_execute(task, data):
    if not data:
        raise ValueError('Missing data')
    return task(data)

def recovery_orchestrator(op, payload):
    try:
        result = secure_execute(op, payload)
        return result if result is not None else 'default_safe_value'
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        return 'recovery_fallback_state'