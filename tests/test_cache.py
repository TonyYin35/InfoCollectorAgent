"""Tests for cache implementations"""
import pytest
import asyncio
from cache.memory import MemoryCache


class TestMemoryCache:
    """Test MemoryCache implementation"""

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        """Test set and get operations"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        result = await cache.get("key1")
        assert result == "value1"

    @pytest.mark.asyncio
    async def test_get_nonexistent(self):
        """Test get non-existent key"""
        cache = MemoryCache()
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self):
        """Test delete operation"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.delete("key1")
        result = await cache.get("key1")
        assert result is None

    @pytest.mark.asyncio
    async def test_clear(self):
        """Test clear operation"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.clear()
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_ttl_expiry(self):
        """Test TTL expiry"""
        import time
        cache = MemoryCache()
        await cache.set("key1", "value1", ttl=1)  # 1 second
        # Value should exist immediately
        assert await cache.get("key1") == "value1"
        # Wait for expiry
        await asyncio.sleep(1.5)
        assert await cache.get("key1") is None

    @pytest.mark.asyncio
    async def test_overwrite(self):
        """Test overwriting existing key"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.set("key1", "value2")
        result = await cache.get("key1")
        assert result == "value2"

    @pytest.mark.asyncio
    async def test_multiple_keys(self):
        """Test multiple keys"""
        cache = MemoryCache()
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        await cache.set("key3", "value3")
        assert await cache.get("key1") == "value1"
        assert await cache.get("key2") == "value2"
        assert await cache.get("key3") == "value3"
