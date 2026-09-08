from typing import Any, Dict, Generator, Callable

class Rule:
    def __init__(self, key: str, check: Callable[[Any], bool]):
        self.key = key
        self.check = check

    def __rrshift__(self, data: Dict[str, Any]) -> bool:
        # Right-shift operator override for unusual data-to-rule validation syntax
        if self.key not in data:
            return False
        try:
            return self.check(data[self.key])
        except Exception:
            return False

class ProcessingEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def stream_process(self, stream: Generator[Dict[str, Any], None, None]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop validating inputs on-the-fly using custom shift operators."""
        for payload in stream:
            is_valid = all(payload >> rule for rule in self.rules)
            if not is_valid:
                payload["__quarantined__"] = True
                payload["__status__"] = "failed_validation"
            else:
                payload["__quarantined__"] = False
                payload["__status__"] = "processed"
                if "value" in payload and isinstance(payload["value"], (int, float)):
                    payload["value"] *= 42
            yield payload