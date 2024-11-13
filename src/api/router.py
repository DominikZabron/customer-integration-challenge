from typing import List

import duckdb
from fastapi import APIRouter, Depends, HTTPException

from .database import get_db
from .models import ProductResponse
from .services import ProductService

router = APIRouter(prefix="/v1")


@router.get(
    "/product/{upc}",
    response_model=List[ProductResponse],
    description="Get detailed product information by UPC",
    responses={
        404: {"description": "Product not found"},
        422: {"description": "Invalid UPC format"},
    },
)
async def get_product(upc: str, conn: duckdb.DuckDBPyConnection = Depends(get_db)):
    service = ProductService(conn)

    products = service.get_product_variants_by_upc(upc)
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    return products
