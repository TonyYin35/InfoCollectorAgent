"""Dependency injection for API routes"""
from cache.base import CacheBackend
from cache.memory import cache


async def get_cache() -> CacheBackend:
    """Get cache backend - can be swapped for Redis, etc."""
    return cache
