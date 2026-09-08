import inspect
from typing import Any, Callable, Dict, List


class CorePipeline:
    """Dynamic pipeline core that auto-organizes step execution order."""

    def __init__(self, name: str = "main") -> None:
        self.name = name
        self._registry: Dict[int, List[Callable[..., Any]]] = {}

    def step(self, priority: int = 50) -> Callable:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._registry.setdefault(priority, []).append(func)
            return func

        return decorator

    def __getitem__(self, priority: int) -> List[Callable[..., Any]]:
        return self._registry.get(priority, [])

    def execute(self, initial_value: Any) -> Any:
        state = initial_value
        ordered_steps = [
            fn
            for prio in sorted(self._registry.keys())
            for fn in self._registry[prio]
        ]

        for fn in ordered_steps:
            sig = inspect.signature(fn)
            if len(sig.parameters) == 0:
                state = fn()
            else:
                state = fn(state)
        return state

    def __call__(self, initial_value: Any) -> Any:
        return self.execute(initial_value)


kernel = CorePipeline()


def reorganize_pipeline(
    pipeline: CorePipeline, priority_map: Dict[Callable, int]
) -> CorePipeline:
    """Re-organizes pipeline steps according to a new priority mapping."""
    reorganized = CorePipeline(name=f"{pipeline.name}_reorganized")
    all_steps = [fn for steps in pipeline._registry.values() for fn in steps]

    for fn in all_steps:
        prio = priority_map.get(fn, 50)
        reorganized.step(priority=prio)(fn)

    return reorganized
