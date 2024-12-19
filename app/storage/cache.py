from redis.asyncio import ConnectionPool, Redis
from decimal import Decimal
import hashlib

class CacheManager:
    def __init__(self, redis_url: str):
        self.pool = ConnectionPool.from_url(redis_url, max_connections=10, decode_responses=True)
        self.redis = Redis(connection_pool=self.pool)

    def _generate_cache_key(self, product_title: str, image_url: str) -> str:
        composite_key = f"{product_title}:{image_url}"
        return hashlib.md5(composite_key.encode()).hexdigest()

    async def get_cached_price(self, product_title: str, image_url: str) -> Decimal | None:
        cache_key = self._generate_cache_key(product_title, image_url)
        price = await self.redis.get(cache_key)
        return Decimal(price) if price else None

    async def cache_price(self, product_title: str, image_url: str, price: Decimal) -> None:
        cache_key = self._generate_cache_key(product_title, image_url)
        await self.redis.set(cache_key, str(price))
