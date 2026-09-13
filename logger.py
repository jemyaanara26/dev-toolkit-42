import sys
import traceback
from typing import Any

class BoundaryResilientLogger:
    def __init__(self, fallback_stream=sys.stderr):
        self.fallback = fallback_stream
        self._in_logging = False

    def emit(self, level: str, raw_payload: Any) -> None:
        if self._in_logging:
            return
        self._in_logging = True
        try:
            try:
                text = str(raw_payload)
            except Exception as repr_err:
                text = f"[unrepresentable payload: {type(raw_payload).__name__} ({repr_err})]"

            entry = f"[{level.upper()}] {text.encode('utf-8', errors='backslashreplace').decode('utf-8')}\n"
            
            try:
                self.fallback.write(entry)
                self.fallback.flush()
            except (AttributeError, IOError, ValueError):
                try:
                    sys.__stderr__.write(entry)
                    sys.__stderr__.flush()
                except Exception:
                    pass
        finally:
            self._in_logging = False

    def info(self, data: Any) -> None:
        self.emit("info", data)

    def error(self, data: Any, exc: Exception = None) -> None:
        payload = f"{data} (Exc: {exc})" if exc else data
        self.emit("error", payload)
