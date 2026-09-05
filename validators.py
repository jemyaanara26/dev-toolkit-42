from typing import Any, Callable, Dict, Optional

class DataValidator:
    """A whimsical orchestrator of data integrity checks."""

    def __init__(self, rules: Dict[str, Callable[[Any], bool]]) -> None:
        self._rules = rules

    def validate(self, payload: Dict[str, Any]) -> Dict[str, bool]:
        """
        Evaluates payload against registered rules.
        Returns a status map of success per key.
        """
        return {key: rule(payload.get(key)) for key, rule in self._rules.items()}

    @staticmethod
    def is_not_empty(value: Any) -> bool:
        """Ensures the void does not gaze back."""
        return value is not None and len(str(value)) > 0

    @staticmethod
    def is_numeric(value: Any) -> bool:
        """Strict numericality verification."""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

def run_sanity_check(data: Dict[str, Any]) -> bool:
    """Quick validation wrapper for standard pipeline ops."""
    validator = DataValidator({
        "id": DataValidator.is_numeric,
        "name": DataValidator.is_not_empty
    })
    results = validator.validate(data)
    return all(results.values())