from pathlib import Path

import duckdb


def load_data(conn: duckdb.DuckDBPyConnection, data_dir: str = "input_data"):
    """Load data from CSV files directly into DuckDB"""
    data_path = Path(data_dir)

    conn.execute(
        f"""
        CREATE OR REPLACE TABLE meta_raw AS 
        SELECT * FROM read_csv_auto('{data_path / 'coding_challenge_meta.csv'}');
        
        CREATE OR REPLACE TABLE inventory_raw AS 
        SELECT * FROM read_csv_auto('{data_path / 'coding_challenge_inventory.csv'}');
        
        CREATE OR REPLACE TABLE prices_raw AS 
        SELECT * FROM read_csv_auto('{data_path / 'coding_challenge_prices.csv'}');
    """
    )


def create_views(conn: duckdb.DuckDBPyConnection):
    """Create normalized views of the raw data"""

    # Create normalized view of metadata with GTIN-14 formatted UPCs
    conn.execute(
        """
        CREATE OR REPLACE VIEW meta_normalized AS
        SELECT 
            LPAD(CAST(product_upc AS VARCHAR), 14, '0') as upc,
            item_number,
            item_description as name,
            CASE 
                WHEN case_upc IS NOT NULL
                THEN LPAD(CAST(case_upc AS VARCHAR), 14, '0')
            END as case_upc,
            CAST(case_pack AS INTEGER) as case_pack,
            supplier
        FROM meta_raw
        WHERE product_upc IS NOT NULL
    """
    )

    # Create view combining inventory date and time
    conn.execute(
        """
        CREATE OR REPLACE VIEW inventory_normalized AS
        SELECT 
            item_number,
            inventory_level,
            CAST(report_date || ' ' || report_time AS TIMESTAMP) as inventory_updated_at
        FROM inventory_raw
    """
    )


def process_products(conn: duckdb.DuckDBPyConnection):
    """Process and insert main products"""
    conn.execute(
        """
        INSERT INTO products (
            product_id,upc, name, item_number, price, supplier, 
            inventory_level, inventory_updated_at
        )
        SELECT DISTINCT ON (m.upc)
            row_number() OVER () as product_id,
            m.upc,
            m.name,
            m.item_number,
            p.price,
            m.supplier,
            COALESCE(i.inventory_level, 0),
            i.inventory_updated_at
        FROM meta_normalized m
        LEFT JOIN prices_raw p ON LPAD(CAST(product_upc AS VARCHAR), 14, '0') = m.upc
        LEFT JOIN inventory_normalized i ON i.item_number = m.item_number
        WHERE m.upc IS NOT NULL
    """
    )


def process_alternates(conn: duckdb.DuckDBPyConnection):
    """Process and insert product alternates (cases and variants)"""

    # Insert case alternates
    conn.execute(
        """
        INSERT INTO product_alternates (
            product_alternate_id, product_id, upc, alternate_type, case_pack
        )
        SELECT 
            row_number() OVER () as product_alternate_id,
            p.product_id,
            m.case_upc,
            'case',
            m.case_pack
        FROM meta_normalized m
        JOIN products p ON p.upc = m.upc
        WHERE m.case_upc IS NOT NULL
    """
    )

    # Insert variant alternates
    conn.execute(
        """
        WITH variants AS (
            SELECT 
                m1.upc,
                m2.item_number as variant_item_number
            FROM meta_normalized m1
            JOIN meta_normalized m2 
                ON m1.upc = m2.upc 
                AND m1.item_number != m2.item_number
        )
        INSERT INTO product_alternates (
            product_alternate_id, product_id, upc, alternate_type
        )
        SELECT DISTINCT
            row_number() OVER () + (SELECT COALESCE(MAX(product_alternate_id), 0) FROM product_alternates) as product_alternate_id,
            p.product_id,
            v.upc,
            'variant'
        FROM variants v
        JOIN products p ON p.upc = v.upc
        WHERE v.upc NOT IN (SELECT upc FROM product_alternates)
    """
    )


def validate_data(conn: duckdb.DuckDBPyConnection) -> list:
    """Validate data quality and return any issues found"""
    issues = []

    # Check for invalid UPCs
    invalid_upcs = conn.execute(
        """
        SELECT upc FROM products 
        WHERE LENGTH(upc) != 14 OR upc NOT REGEXP '^\d{14}$'
    """
    ).fetchall()
    if invalid_upcs:
        issues.append(f"Found {len(invalid_upcs)} invalid UPCs")

    # Check for missing prices
    missing_prices = conn.execute(
        """
        SELECT COUNT(*) FROM products WHERE price IS NULL
    """
    ).fetchone()[0]
    if missing_prices:
        issues.append(f"Found {missing_prices} products without prices")

    # Check for negative inventory
    negative_inventory = conn.execute(
        """
        SELECT COUNT(*) FROM products WHERE inventory_level < 0
    """
    ).fetchone()[0]
    if negative_inventory:
        issues.append(f"Found {negative_inventory} products with negative inventory")

    return issues
