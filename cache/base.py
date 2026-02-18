from typing import Protocol, Optional


class CacheBackend(Protocol):
    """Cache backend interface - can be replaced with Redis, Memcached, etc."""

    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        ...

    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        """Set key-value pair with optional TTL in seconds"""
        ...

    async def delete(self, key: str) -> None:
        """Delete key"""
        ...

    async def clear(self) -> None:
        """Clear all cache"""
        ...
