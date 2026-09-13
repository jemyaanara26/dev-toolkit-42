from typing import Any, Callable, Dict, Union, List

class Harmonizer:
    """A creative utility to clean, prune, and safely traverse messy nested data structures."""
    
    def __init__(self, data: Union[Dict, List]):
        self.data = data

    def prune(self, condition: Callable[[Any], bool] = lambda v: v in (None, "", [], {})) -> 'Harmonizer':
        """Recursively removes keys/values matching the condition."""
        def _clean(node: Any) -> Any:
            if isinstance(node, dict):
                return {k: _clean(v) for k, v in node.items() if not condition(v) and _clean(v) is not None}
            elif isinstance(node, list):
                return [_clean(x) for x in node if not condition(x) and _clean(x) is not None]
            return node
        
        self.data = _clean(self.data) or {}
        return self

    def navigate(self, path: str, default: Any = None) -> Any:
        """Safely extracts nested data using dot-notation path."""
        parts = path.split('.')
        current = self.data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
                current = current[int(part)]
            else:
                return default
        return current

    def morph(self, transformer: Callable[[Any], Any]) -> 'Harmonizer':
        """Applies a transformation function to all leaf values in the data structure."""
        def _traverse(node: Any) -> Any:
            if isinstance(node, dict):
                return {k: _traverse(v) for k, v in node.items()}
            elif isinstance(node, list):
                return [_traverse(x) for x in node]
            return transformer(node)
        
        self.data = _traverse(self.data)
        return self

    def collect(self) -> Union[Dict, List]:
        """Returns the final processed structure."""
        return self.data