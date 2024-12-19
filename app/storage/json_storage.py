import json
import os
from typing import List
from decimal import Decimal
from .base import BaseStorage
from app.models.product import Product

class JsonStorage(BaseStorage):
    def __init__(self, file_path: str = "products.json"):
        self.file_path = file_path

    async def save_products(self, products: List[Product]) -> None:
        with open(self.file_path, 'w') as f:
            products_data = [
                {
                    "product_title": p.product_title.encode('ascii', 'ignore').decode(),  # Remove non-ASCII chars
                    "product_price": float(p.product_price),  # Convert Decimal to float
                    "path_to_image": p.path_to_image
                }
                for p in products
            ]
            json.dump(products_data, f, indent=2)

    async def get_products(self) -> List[Product]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return [Product(**item) for item in data]
