from dataclasses import dataclass
from typing import List

from parsers.writer import CSVWriter


@dataclass
class ParserResult:
    parser_name: str
    failed_rows: List[tuple[int, List[str]]]
    modified_rows: List[tuple[int, List[str], List[str]]]
    validated_rows: List[List[str]]
    total_processed: int
    input_file: str

    def write(self, ops_dir: str = None):
        """Write both operational logs and validated data"""
        writer = CSVWriter(
            parser_name=self.parser_name,
            failed_rows=self.failed_rows,
            modified_rows=self.modified_rows,
            validated_rows=self.validated_rows,
            input_file=self.input_file,
        )
        writer.write_ops(ops_dir)
        writer.write_validated()
