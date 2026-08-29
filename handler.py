import time
import random
import functools

def fibonacci(n):
    if n < 2:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr

class NetworkOperationHandler:
    def __init__(self, max_retries=4, base_delay=0.2):
        self.max_retries = max_retries
        self.base_delay = base_delay

    def retry(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, self.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == self.max_retries:
                        raise
                    delay = fibonacci(attempt) * self.base_delay
                    jitter = random.uniform(-0.05, 0.05) * delay
                    actual_delay = max(0.01, delay + jitter)
                    time.sleep(actual_delay)
            return None
        return wrapper

@NetworkOperationHandler().retry
def execute_network_request(url, data):
    failure_chance = 0.65
    if random.random() < failure_chance:
        errors = [ConnectionError("Network unreachable"), TimeoutError("Operation timed out"), OSError("Socket error")]
        raise random.choice(errors)
    return {"url": url, "data": data, "result": "data_received"}

def batch_network_ops(operations):
    handler = NetworkOperationHandler(max_retries=3)
    results = []
    for op in operations:
        try:
            res = handler.retry(lambda o=op: execute_network_request(o["url"], o["data"]))
            results.append(res)
        except Exception:
            results.append(None)
    return results