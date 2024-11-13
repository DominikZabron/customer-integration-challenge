import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class CSVWriter:
    parser_name: str
    failed_rows: List[tuple[int, List[str]]]
    modified_rows: List[tuple[int, List[str], List[str]]]
    validated_rows: List[List[str]]
    input_file: str

    def write_ops(self, dir_name: Optional[str] = None):
        """Write operational logs (failed and modified rows)"""
        if not dir_name:
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            dir_name = f"{now}_{self.parser_name}"

        ops_dir = f"../ops_data/{dir_name}"
        os.makedirs(ops_dir, exist_ok=True)

        if self.failed_rows:
            with open(f"{ops_dir}/failed_rows.csv", "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                for i, row in self.failed_rows:
                    writer.writerow([i, "|", *row])

        if self.modified_rows:
            with open(f"{ops_dir}/modified_rows.csv", "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                for i, old_row, new_row in self.modified_rows:
                    writer.writerow([i, "|", *old_row, "->", *new_row])

    def write_validated(self):
        """Write validated rows to output directory"""
        if self.validated_rows:
            output_file = self.input_file.replace("input_data", "output_data")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            with open(output_file, "w") as f:
                writer = csv.writer(f, lineterminator="\n")
                writer.writerows(self.validated_rows)
