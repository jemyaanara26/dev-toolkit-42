from typing import Callable, Any, TypeVar, Generic, Dict, List

T = TypeVar("T")
R = TypeVar("R")

class MorphPipeline(Generic[T, R]):
    """A fluent pipeline for transforming data structures with lazy evaluation semantics."""

    def __init__(self, initial_data: T) -> None:
        """Initialize the pipeline with a primary payload."""
        self._payload: T = initial_data
        self._transforms: List[Callable[[Any], Any]] = []

    def morph(self, fn: Callable[[Any], Any]) -> "MorphPipeline[T, Any]":
        """Queue a transformation step into the morphing pipeline.

        Args:
            fn: Transformation function accepting payload and returning modified state.
        """
        self._transforms.append(fn)
        return self

    def resolve(self) -> Any:
        """Execute queued transformations iteratively over the payload.

        Returns:
            The fully transformed result after applying all staged functions.
        """
        current: Any = self._payload
        for step in self._transforms:
            current = step(current)
        return current

    def __or__(self, fn: Callable[[Any], Any]) -> "MorphPipeline[T, Any]":
        """Overload bitwise OR operator to allow pipe syntax (pipeline | transform)."""
        return self.morph(fn)


def deep_flatten(dictionary: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Recursively flatten a nested dictionary into single-level dot-separated key-value pairs.

    Args:
        dictionary: The nested dictionary to flatten.
        parent_key: The accumulated prefix key from higher recursion levels.
        sep: Separator character joining nested key names.

    Returns:
        A flattened single-depth dictionary.
    """
    items: List[tuple[str, Any]] = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(deep_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
