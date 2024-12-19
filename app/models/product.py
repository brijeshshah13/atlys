from pydantic import BaseModel, HttpUrl
from decimal import Decimal
from typing import Optional

class Product(BaseModel):
    product_title: str
    product_price: Decimal
    path_to_image: str

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)  # Convert Decimal to float for JSON serialization
        }

class ScrapingConfig(BaseModel):
    page_limit: Optional[int] = None
    proxy: Optional[str] = None
