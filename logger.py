import sys
from queue import Queue
from threading import Thread

class FastLogger:
    """A high-performance logger that defers string formatting to a background thread."""
    def __init__(self, stream=None):
        self.stream = stream or sys.stdout
        self.queue = Queue(maxsize=5000)
        self.worker = Thread(target=self._consume, daemon=True)
        self.worker.start()

    def _consume(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            fmt, args, kwargs = item
            try:
                resolved = fmt.format(*args, **kwargs) if (args or kwargs) else str(fmt)
                self.stream.write(resolved + "\n")
            except Exception as err:
                self.stream.write(f"Logging error: {err}\n")
            finally:
                self.queue.task_done()

    def emit(self, msg, *args, **kwargs):
        try:
            self.queue.put_nowait((msg, args, kwargs))
        except Exception:
            pass

    def shutdown(self):
        self.queue.put(None)
        self.worker.join()
