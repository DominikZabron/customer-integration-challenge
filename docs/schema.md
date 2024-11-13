# Database Schema Documentation

## Products Table
Stores basic information for products.

| Column | Type | Description |
|--------|------|-------------|
| product_id | INTEGER | Primary Key |
| upc | VARCHAR(14) | GTIN-14 formatted UPC, unique identifier |
| name | VARCHAR | Product name/description |
| item_number | VARCHAR | Customer's internal identifier |
| price | DECIMAL(10,2) | Product price |
| supplier | VARCHAR | Name of supplier |
| inventory_level | INTEGER | Current inventory level |
| inventory_updated_at | TIMESTAMP | Last inventory update time |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record last update time |

## Product Alternates Table
Stores variant and case relationships between products.

| Column | Type | Description |
|--------|------|-------------|
| product_alternate_id | INTEGER | Primary Key |
| product_id | INTEGER | Foreign Key to products table |
| upc | VARCHAR(14) | GTIN-14 formatted UPC for alternate |
| alternate_type | VARCHAR | Either 'variant' or 'case' |
| case_pack | INTEGER | Number of units in case (for case type only) |
| created_at | TIMESTAMP | Record creation time 