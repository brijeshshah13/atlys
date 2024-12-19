from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.product import Product, ScrapingConfig
from app.core.scraper import Scraper
from app.storage.json_storage import JsonStorage
from app.storage.cache import CacheManager
from app.notifications.console import ConsoleNotifier
from app.config import settings
from .auth import verify_token

router = APIRouter()


@router.post("/scrape", response_model=List[Product])
async def scrape_products(config: ScrapingConfig, token: str = Depends(verify_token)):
    storage = JsonStorage()
    cache = CacheManager(settings.REDIS_URL)
    notifier = ConsoleNotifier()

    scraper = Scraper(proxy=config.proxy)
    all_products = []
    updated_count = 0

    try:
        page = 1
        while True:
            if config.page_limit and page > config.page_limit:
                break

            products = await scraper.scrape_page(page)
            if not products:
                break

            for product in products:
                cached_price = await cache.get_cached_price(
                    product.product_title, product.path_to_image
                )
                if cached_price != product.product_price:
                    updated_count += 1
                    await cache.cache_price(
                        product.product_title,
                        product.path_to_image,
                        product.product_price,
                    )

            all_products.extend(products)
            page += 1

        await storage.save_products(all_products)
        await notifier.notify(
            f"Scraping completed. Total products: {len(all_products)}, Updated: {updated_count}"
        )

        return all_products

    finally:
        await scraper.close()
