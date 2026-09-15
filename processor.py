"""Polymorphic stream transformer with lazy processing capabilities."""

from typing import TypeVar, Callable, Generic, Iterable, Generator, Any

T = TypeVar("T")
R = TypeVar("R")


class MorphicProcessor(Generic[T]):
    """A fluent pipeline builder for deferred stream transformations and side-effects."""

    def __init__(self, source: Iterable[T]) -> None:
        """Initialize the stream processor with a primary iterable source."""
        self._iterable: Iterable[T] = source
        self._transforms: list[Callable[[Any], Any]] = []

    def pipe(self, transform: Callable[[Any], R]) -> "MorphicProcessor[R]":
        """Attach a transformation stage to the lazy processing pipeline."""
        self._transforms.append(transform)
        return self  # type: ignore[return-value]

    def tap(self, observer: Callable[[Any], None]) -> "MorphicProcessor[T]":
        """Inject a side-effect observer into the pipeline without altering values."""

        def _tap_wrapper(value: Any) -> Any:
            observer(value)
            return value

        self._transforms.append(_tap_wrapper)
        return self

    def execute(self) -> Generator[Any, None, None]:
        """Yield evaluated items after running all transformations sequentially."""
        for item in self._iterable:
            current: Any = item
            for step in self._transforms:
                current = step(current)
            yield current

    def collect(self) -> list[Any]:
        """Drain the pipeline stream into a collected list output."""
        return list(self.execute())


def batch_stream(data: Iterable[T], size: int = 3) -> Generator[list[T], None, None]:
    """Chunk an incoming iterable stream into fixed-size window batches."""
    batch: list[T] = []
    for item in data:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
