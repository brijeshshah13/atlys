import asyncio
from functools import wraps
from typing import Callable
from app.config import settings

def async_retry(max_attempts: int = settings.RETRY_ATTEMPTS, delay: int = settings.RETRY_DELAY):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    await asyncio.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator
