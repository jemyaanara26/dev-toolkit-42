import types
from typing import Callable, Any, List, Dict


class FusedPipeline:
    """Dynamic pipeline optimizer that fuses chained functions into single compiled code."""

    def __init__(self, name: str = "optimized_pipeline"):
        self.name = name
        self._stages: List[Callable[[Any], Any]] = []

    def add_stage(self, fn: Callable[[Any], Any]) -> "FusedPipeline":
        self._stages.append(fn)
        return self

    def compile(self) -> Callable[[Any], Any]:
        if not self._stages:
            return lambda x: x

        globs: Dict[str, Any] = {}
        lines = ["def _fused_entry(data):"]

        for idx, stage in enumerate(self._stages):
            var_name = f"_fn_{idx}"
            globs[var_name] = stage
            prev_var = "data" if idx == 0 else f"val_{idx - 1}"
            curr_var = f"val_{idx}"
            lines.append(f"    {curr_var} = {var_name}({prev_var})")

        lines.append(f"    return val_{len(self._stages) - 1}")
        code_str = "\n".join(lines)

        code_obj = compile(code_str, f"<fused_{id(self)}>", "exec")
        namespace: Dict[str, Any] = {}
        exec(code_obj, globs, namespace)
        return namespace["_fused_entry"]


class CoreEngine:
    """Central execution engine with runtime byte-code compilation optimizations."""

    def __init__(self):
        self._pipeline_cache: Dict[int, Callable[[Any], Any]] = {}

    def fast_execute(self, initial_value: Any, *transforms: Callable[[Any], Any]) -> Any:
        key = hash(tuple(id(t) for t in transforms))
        if key not in self._pipeline_cache:
            pipeline = FusedPipeline()
            for t in transforms:
                pipeline.add_stage(t)
            self._pipeline_cache[key] = pipeline.compile()
        return self._pipeline_cache[key](initial_value)

    def batch_process(self, items: List[Any], transform: Callable[[Any], Any]) -> List[Any]:
        fast_map = map
        return list(fast_map(transform, items))
