# Data Processing System

A Python-based system for parsing CSV files, transforming data, and serving it through an API. The system processes inventory, product metadata, and pricing information through a pipeline of parsing, transformation, and API serving.

## Prerequisites

- Python 3.12+
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. CSV Parser

The system includes three specialized parsers:

- `InventoryParser`: Processes inventory levels with timestamps
- `MetaParser`: Handles product metadata and supplier information
- `PriceParser`: Manages product pricing data

Place your input files in the `input_data/` directory:
```
input_data/
├── coding_challenge_inventory.csv
├── coding_challenge_meta.csv
└── coding_challenge_prices.csv
```

Run the parser:
```python
from src.main import parse_input_files

parse_input_files()
```

Parsed results will be saved in the `output_data/` directory.

### 2. Data Transformations

The transformation module loads parsed data into a DuckDB database and performs necessary data processing:

```python
from src.main import transform_data

# Using default paths
transform_data()

# Using custom paths
transform_data(
    db_path="custom/path/database.duckdb",
    data_dir="custom/path/output_data"
)
```

The transformation pipeline:
1. Creates database schema
2. Loads parsed CSV data
3. Creates database views
4. Processes product relationships
5. Generates alternate product mappings

### 3. API

The API provides access to the processed data through a RESTful interface.

Start the API server:
```bash
python src/api/app.py
```

Available endpoint:
- `GET /products/{upc}` - Get specific product details

API Documentation:
- Interactive Swagger UI: `http://localhost:8000/docs`

## Project Structure

```
├── input_data/          # Raw CSV files
├── ops_data/            # Intermediate data (optional)
├── output_data/         # Processed CSV files
├── src/
│   ├── api/            # FastAPI implementation
│   ├── parsers/        # CSV parsing logic
│   └── transformers/   # Data transformation logic
│   └── main.py         # Main entry point
├── requirements.txt
└── README.md
```

## License

MIT License - See LICENSE file for details
