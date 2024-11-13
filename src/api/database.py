from typing import Generator

import duckdb


def get_db() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    conn = duckdb.connect("product_db.duckdb")
    try:
        yield conn
    finally:
        conn.close()
