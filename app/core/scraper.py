import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
import os
import aiofiles
from urllib.parse import urlparse
from app.models.product import Product
from .retry import async_retry
from app.config import settings

class Scraper:
    def __init__(self, proxy: Optional[str] = None):
        self.base_url = settings.BASE_URL
        self.images_dir = "images"
        os.makedirs(self.images_dir, exist_ok=True)
        if proxy:
            if not proxy.startswith(('http://', 'https://')):
                proxy = f'http://{proxy}'
        self.proxy = proxy
        self.client = httpx.AsyncClient(
            proxies=proxy if proxy else None,
            verify=False,
            timeout=30.0
        )

    async def download_image(self, image_url: str) -> str:
        filename = os.path.basename(urlparse(image_url).path)
        local_path = os.path.join(self.images_dir, filename)
        
        if not os.path.exists(local_path):
            response = await self.client.get(image_url)
            async with aiofiles.open(local_path, 'wb') as f:
                await f.write(response.content)
        
        return local_path

    @async_retry()
    async def scrape_page(self, page: int) -> List[Product]:
        url = self.base_url if page == 1 else f"{self.base_url}page/{page}/"
        response = await self.client.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        products_container = soup.select('div.mf-shop-content ul.products li.product')
        
        for product in products_container:
            try:
                name = product.select_one('h2.woo-loop-product__title a').text.strip()
                name = name.encode('ascii', 'ignore').decode()
                
                price_element = product.select_one('span.price ins .woocommerce-Price-amount bdi')
                if not price_element:
                    price_element = product.select_one('span.price .woocommerce-Price-amount bdi')
                
                price = price_element.contents[-1].strip()
                
                img_element = product.select_one('img')
                image_url = (
                    img_element.get('data-lazy-src') or 
                    img_element.get('data-src') or 
                    img_element.get('src')
                )
                
                local_image_path = await self.download_image(image_url)
                
                products.append(Product(
                    product_title=name,
                    product_price=price,
                    path_to_image=local_image_path
                ))
            except Exception as e:
                print(f"Error processing product: {e} {product}")
                continue
                
        return products

    async def close(self):
        await self.client.aclose()
