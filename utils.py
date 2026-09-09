import functools
import time
import collections

class MemoizedLRU:
    def __init__(self, maxsize=128):
        self.cache = collections.OrderedDict()
        self.maxsize = maxsize

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.cache.move_to_end(key)
            if len(self.cache) > self.maxsize:
                self.cache.popitem(last=False)
            return result
        return wrapper

def batch_process(data, chunk_size=1000):
    it = iter(data)
    return iter(lambda: list(itertools.islice(it, chunk_size)), [])

import itertools

def fast_flatten(nested_list):
    return list(itertools.chain.from_iterable(nested_list))

def profile_execution(func):
    @functools.wraps(func)
    def timed(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        return result, time.perf_counter() - start
    return timed