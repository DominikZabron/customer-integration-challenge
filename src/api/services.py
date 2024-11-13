from typing import List, Optional

import duckdb

from .models import ProductResponse, ProductVariant


class ProductService:
    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn

    def get_product_by_upc(self, upc: str) -> Optional[dict]:
        # Try to find product either directly or through alternates
        result = self.conn.execute(
            """
            WITH base_product AS (
                -- Find product_id either from products or alternates
                SELECT DISTINCT p.product_id
                FROM products p
                LEFT JOIN product_alternates pa ON pa.product_id = p.product_id
                WHERE p.upc = ? OR pa.upc = ?
            )
            SELECT 
                p.upc,
                p.name,
                p.item_number,
                p.price,
                p.supplier,
                p.inventory_level,
                p.inventory_updated_at
            FROM products p 
            WHERE p.product_id IN (SELECT product_id FROM base_product)
        """,
            [upc, upc],
        ).fetchall()

        if not result:
            return None

        # Return all matching products
        return [
            dict(
                zip(
                    [
                        "upc",
                        "name",
                        "item_number",
                        "price",
                        "supplier",
                        "inventory_level",
                        "inventory_updated_at",
                    ],
                    row,
                )
            )
            for row in result
        ]

    def get_variants(self, product_id: int) -> List[ProductVariant]:
        results = self.conn.execute(
            """
            SELECT 
                pa.upc,
                pa.alternate_type as type,
                pa.case_pack
            FROM product_alternates pa
            WHERE pa.product_id = ?
        """,
            [product_id],
        ).fetchall()

        return [
            ProductVariant(upc=row[0], type=row[1], case_pack=row[2]) for row in results
        ]

    def get_product_variants_by_upc(self, upc: str) -> List[ProductResponse]:
        # Get product_id from either products or alternates
        product_id_results = self.conn.execute(
            """
            SELECT DISTINCT p.product_id
            FROM products p
            LEFT JOIN product_alternates pa ON pa.product_id = p.product_id
            WHERE p.upc = ? OR pa.upc = ?
        """,
            [upc, upc],
        ).fetchall()

        if not product_id_results:
            return None

        all_variants = []
        for product_id_result in product_id_results:
            product_id = product_id_result[0]
            variants = self.get_variants(product_id)
            all_variants.extend(variants)

        # Get all related products
        products = self.get_product_by_upc(upc)
        if not products:
            return None

        # Return all products with their variants
        return [
            ProductResponse(**product, variants=all_variants) for product in products
        ]
