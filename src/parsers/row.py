from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Row:
    raw_row: List[str]

    @classmethod
    def from_line(cls, line: str, delimiter: str = ",") -> "Row":
        return cls(raw_row=line.strip().split(delimiter))

    def __post_init__(self):
        self._row = self.raw_row.copy()
        self.new_row = []
        self._iter_index = 0
        self._current_value = None

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self._iter_index >= len(self._row):
            raise StopIteration
        self._current_value = self._row[self._iter_index]
        self._iter_index += 1
        return self._current_value

    def push_back(self):
        if self._iter_index > 0:
            self._iter_index -= 1

    def append(self, value: Optional[str] = None):
        """Append current value or its modified version to new_row"""
        self.new_row.append(value)

    @property
    def was_modified(self) -> bool:
        return self.raw_row != self.new_row
