from dataclasses import dataclass
from typing import List

from tqdm import tqdm

from parsers.field import Field
from parsers.result import ParserResult
from parsers.row import Row


@dataclass
class CSVParser:
    file_path: str
    delimiter: str = ","

    def _get_fields(self) -> List[Field]:
        """Get all Field instances defined in the parser class"""
        return [
            field
            for field in self.__class__.__dict__.values()
            if isinstance(field, Field)
        ]

    def ingest(self) -> ParserResult:
        failed_rows: List[tuple[int, List[str]]] = []
        modified_rows: List[tuple[int, List[str], List[str]]] = []
        validated_rows: List[List[str]] = []
        fields = self._get_fields()

        with open(self.file_path, "r", encoding="utf-8") as file:
            for i, line in enumerate(tqdm(file)):
                row = Row.from_line(line, self.delimiter)

                if i == 0:
                    header = row.raw_row
                    validated_rows.append(header)
                    continue

                value = None

                for field in fields:
                    if not value:
                        try:
                            value = next(row)
                        except StopIteration:
                            value = None

                    if not field.validate(value):
                        if field.required:
                            failed_rows.append((i, row.raw_row))
                            break
                        else:
                            if value:
                                row.push_back()
                            value = field.default

                    value = field.modify(value)
                    row.append(value)
                    value = None

                if len(row.new_row) == len(fields):
                    if row.was_modified:
                        modified_rows.append((i, row.raw_row, row.new_row))
                    validated_rows.append(row.new_row)

        return ParserResult(
            parser_name=self.__class__.__name__,
            failed_rows=failed_rows,
            modified_rows=modified_rows,
            validated_rows=validated_rows,
            total_processed=i + 1,
            input_file=self.file_path,
        )
