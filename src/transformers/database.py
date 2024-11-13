import duckdb


def get_db_connection(db_path: str = "product_db.duckdb") -> duckdb.DuckDBPyConnection:
    """Create or connect to a DuckDB database"""
    return duckdb.connect(db_path)


def create_tables(conn: duckdb.DuckDBPyConnection):
    """Create the required database tables"""

    conn.execute(
        """
        DROP TABLE IF EXISTS product_alternates;
        DROP TABLE IF EXISTS products;
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            upc VARCHAR(14) NOT NULL UNIQUE,
            name VARCHAR NOT NULL,
            item_number VARCHAR NOT NULL,
            price DECIMAL(10,2),
            supplier VARCHAR,
            inventory_level INTEGER,
            inventory_updated_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT NULL
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS product_alternates (
            product_alternate_id INTEGER PRIMARY KEY,
            product_id INTEGER NOT NULL,
            upc VARCHAR(14) NOT NULL,
            alternate_type VARCHAR NOT NULL,
            case_pack INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """
    )
