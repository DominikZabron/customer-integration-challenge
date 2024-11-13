from typing import Generator

from duckdb import DuckDBPyConnection

from ..transformers.database import get_db_connection


def get_db() -> Generator[DuckDBPyConnection, None, None]:
    db = get_db_connection()
    try:
        yield db
    finally:
        db.close()
