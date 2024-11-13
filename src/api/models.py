from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import BaseModel, constr


class ProductVariant(BaseModel):
    upc: str
    type: str
    case_pack: Optional[int] = None


class ProductResponse(BaseModel):
    upc: Annotated[str, constr(pattern=r"^\d{14}$")]
    name: str
    item_number: str
    price: Optional[float] = None
    supplier: Optional[str] = None
    inventory_level: int = 0
    inventory_updated_at: Optional[datetime] = None
    variants: List[ProductVariant]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Product",
                "item_number": "12345",
                "price": 19.99,
                "supplier": "Sample Supplier",
                "inventory_level": 42,
                "inventory_updated_at": "2024-01-01T12:00:00",
                "upc": "00012345678901",
                "variants": [
                    {"upc": "00012345678901", "type": "variant", "case_pack": None},
                    {"upc": "00012345678902", "type": "case", "case_pack": 12},
                ],
            }
        }
