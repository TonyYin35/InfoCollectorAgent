import asyncio
from typing import Optional
import time
from .base import CacheBackend


class MemoryCache:
    """In-memory cache implementation (default)"""

    def __init__(self):
        self._store: dict[str, tuple[str, float]] = {}  # key -> (value, expire_at)
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[str]:
        async with self._lock:
            if key not in self._store:
                return None
            value, expire_at = self._store[key]
            if expire_at > 0 and expire_at < time.time():
                del self._store[key]
                return None
            return value

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        async with self._lock:
            expire_at = time.time() + ttl if ttl > 0 else 0
            self._store[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._store.clear()


# Default cache instance
cache = MemoryCache()
