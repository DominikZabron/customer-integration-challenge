from pathlib import Path

from parsers import (
    CSVParser,
    Field,
    is_digit,
    is_float,
    is_hms_time,
    is_string,
    is_ymd_date,
    negative_to_zero,
    shrink_on_hash,
    shrink_on_spaces,
    to_int,
)
from transformers import (
    create_tables,
    create_views,
    get_db_connection,
    load_data,
    process_alternates,
    process_products,
)


class InventoryParser(CSVParser):
    item_number = Field(required=True, validators=[is_digit], modifiers=[to_int])
    inventory_level = Field(
        required=True, validators=[is_digit], modifiers=[to_int, negative_to_zero]
    )
    report_date = Field(required=True, validators=[is_ymd_date])
    report_time = Field(required=True, validators=[is_hms_time])


class MetaParser(CSVParser):
    product_upc = Field(required=True, validators=[is_digit], modifiers=[to_int])
    item_number = Field(required=True, validators=[is_digit])
    item_description = Field(validators=[is_string])
    case_upc = Field(validators=[is_digit])
    case_pack = Field(validators=[is_float])
    department = Field(validators=[is_digit])
    supplier = Field(
        validators=[is_string], modifiers=[shrink_on_hash, shrink_on_spaces]
    )


class PriceParser(CSVParser):
    product_upc = Field(required=True, validators=[is_digit])
    price = Field(required=True, validators=[is_float])


def parse_input_files():
    """Parse the input CSV files and write the processed results"""
    inventory_result = InventoryParser(
        file_path="input_data/coding_challenge_inventory.csv"
    ).ingest()
    inventory_result.write()

    meta_result = MetaParser(file_path="input_data/coding_challenge_meta.csv").ingest()
    meta_result.write()

    price_result = PriceParser(
        file_path="input_data/coding_challenge_prices.csv"
    ).ingest()
    price_result.write()


def transform_data(db_path: str = "product_db.duckdb", data_dir: str = "output_data"):
    """Transform and load the data into the database"""
    # Create database directory if it doesn't exist
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # Get database connection
    conn = get_db_connection(db_path)

    try:
        # Create tables
        create_tables(conn)

        # Load and process data
        load_data(conn, data_dir)
        create_views(conn)
        process_products(conn)
        process_alternates(conn)

        # Print verification information
        print("\nData import complete!")
        print(
            f"Products count: {conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]}"
        )
        print(
            f"Alternates count: {conn.execute('SELECT COUNT(*) FROM product_alternates').fetchone()[0]}"
        )

    except Exception as e:
        print(f"Error processing data: {e}")
        raise
    finally:
        conn.close()


def main():
    """Main function to run both parsing and transformation steps"""
    print("Step 1: Parsing input files...")
    parse_input_files()

    print("\nStep 2: Transforming data...")
    transform_data()


if __name__ == "__main__":
    main()
