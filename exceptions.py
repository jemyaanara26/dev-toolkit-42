class ToolkitError(Exception):
    """Base exception for dev-toolkit-42."""

class ValidationError(ToolkitError):
    """Raised when inputs fail structural integrity."""

class ConfigurationError(ToolkitError):
    """Raised when system state is invalid."""

class RuntimePanic(ToolkitError):
    """Fatal state requiring immediate circuit breaking."""

class Registry:
    _storage = {}

    @classmethod
    def register(cls, exc_type):
        cls._storage[exc_type.__name__] = exc_type
        return exc_type

    @classmethod
    def spawn(cls, name, *args):
        exc = cls._storage.get(name, ToolkitError)
        return exc(*args)

def guard(condition, exception_type, message):
    """Functional style validation check."""
    if not condition:
        raise exception_type(message)

# Dynamic registration of toolkit exceptions
for _e in [ValidationError, ConfigurationError, RuntimePanic]:
    Registry.register(_e)