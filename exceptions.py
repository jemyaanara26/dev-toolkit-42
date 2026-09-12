import time
from typing import Any, Dict, Tuple, Type


class MetaToolkitError(type):
    """Metaclass ensuring every exception auto-registers in a central registry."""

    registry: Dict[str, Type["ToolkitError"]] = {}

    def __new__(
        mcs, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]
    ):
        cls = super().__new__(mcs, name, bases, namespace)
        mcs.registry[name] = cls
        return cls


class ToolkitError(Exception, metaclass=MetaToolkitError):
    """Structured base exception with dynamic context and payload serialization."""

    def __init__(self, message: str, *, code: int = 500, **details: Any):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details
        self.created_at = time.time()

    def as_payload(self) -> Dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        meta = f" (code={self.code})" if self.code else ""
        extra = f" | {self.details}" if self.details else ""
        return f"[{self.__class__.__name__}]{meta}: {self.message}{extra}"


class ConfigurationError(ToolkitError):
    """Raised when application configuration is invalid or missing."""


class ExecutionPipelineError(ToolkitError):
    """Raised when a task processor encounters an unrecoverable failure."""


class DataValidationError(ToolkitError):
    """Raised when incoming inputs fail validation constraints."""


def synthesize_exception(name: str, base_code: int = 500) -> Type[ToolkitError]:
    """Dynamically generate custom toolkit exceptions at runtime."""
    return type(
        name,
        (ToolkitError,),
        {
            "__init__": lambda self, msg, **kw: ToolkitError.__init__(
                self, msg, code=base_code, **kw
            )
        },
    )
