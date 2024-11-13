from typing import Any, Callable, List


class Field:
    def __init__(
        self,
        required: bool = False,
        default: Any = None,
        validators: List[Callable[[Any], bool]] = None,
        modifiers: List[Callable[[Any], Any]] = None,
    ):
        self.required = required
        self.default = default
        self.validators = validators
        self.modifiers = modifiers

    def validate(self, value: Any) -> Any:
        if not self.validators:
            return True
        return all(validator(value) for validator in self.validators)

    def modify(self, value: Any) -> Any:
        if self.modifiers:
            for modifier in self.modifiers:
                value = modifier(value)
        return value
