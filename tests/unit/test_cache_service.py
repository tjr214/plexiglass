"""
Unit tests for CacheService.

Tests the request caching system with TTL support.
"""

import time
from datetime import datetime, timedelta

import pytest

from plexiglass.services.cache_service import CacheService


class TestCacheServiceInitialization:
    """Test CacheService initialization."""

    def test_creates_cache_service_with_default_ttl(self):
        """Test creating a CacheService with default TTL."""
        cache = CacheService()
        assert cache is not None
        assert cache.default_ttl == 60  # Default 60 seconds

    def test_creates_cache_service_with_custom_ttl(self):
        """Test creating a CacheService with custom TTL."""
        cache = CacheService(default_ttl=120)
        assert cache.default_ttl == 120

    def test_cache_starts_empty(self):
        """Test that cache starts with no entries."""
        cache = CacheService()
        assert cache.size() == 0
        assert cache.is_empty() is True


class TestCacheServiceBasicOperations:
    """Test basic cache operations."""

    def test_set_and_get_value(self):
        """Test setting and getting a cached value."""
        cache = CacheService()
        cache.set("test_key", "test_value")

        result = cache.get("test_key")
        assert result == "test_value"

    def test_get_nonexistent_key_returns_none(self):
        """Test getting a key that doesn't exist."""
        cache = CacheService()
        result = cache.get("nonexistent")
        assert result is None

    def test_set_overwrites_existing_value(self):
        """Test that setting same key overwrites value."""
        cache = CacheService()
        cache.set("key", "value1")
        cache.set("key", "value2")

        result = cache.get("key")
        assert result == "value2"

    def test_has_key_returns_true_for_existing(self):
        """Test has() method for existing key."""
        cache = CacheService()
        cache.set("key", "value")
        assert cache.has("key") is True

    def test_has_key_returns_false_for_nonexistent(self):
        """Test has() method for nonexistent key."""
        cache = CacheService()
        assert cache.has("nonexistent") is False

    def test_delete_removes_key(self):
        """Test deleting a cache entry."""
        cache = CacheService()
        cache.set("key", "value")
        cache.delete("key")

        assert cache.has("key") is False
        assert cache.get("key") is None

    def test_delete_nonexistent_key_does_not_error(self):
        """Test deleting a nonexistent key doesn't raise error."""
        cache = CacheService()
        cache.delete("nonexistent")  # Should not raise

    def test_clear_removes_all_entries(self):
        """Test clearing the entire cache."""
        cache = CacheService()
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")

        cache.clear()

        assert cache.size() == 0
        assert cache.is_empty() is True


class TestCacheServiceTTL:
    """Test TTL (Time-To-Live) functionality."""

    def test_entry_expires_after_ttl(self):
        """Test that cache entry expires after TTL."""
        cache = CacheService(default_ttl=1)  # 1 second TTL
        cache.set("key", "value")

        # Should exist immediately
        assert cache.get("key") == "value"

        # Wait for expiration
        time.sleep(1.1)

        # Should be expired
        assert cache.get("key") is None
        assert cache.has("key") is False

    def test_custom_ttl_per_entry(self):
        """Test setting custom TTL for individual entries."""
        cache = CacheService(default_ttl=60)
        cache.set("key", "value", ttl=2)

        assert cache.get("key") == "value"
        time.sleep(2.1)
        assert cache.get("key") is None

    def test_expired_entries_not_counted_in_size(self):
        """Test that expired entries don't count toward size."""
        cache = CacheService(default_ttl=1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        assert cache.size() == 2

        time.sleep(1.1)

        # Size should reflect cleanup
        assert cache.size() == 0

    def test_get_or_set_with_factory_function(self):
        """Test get_or_set() method with factory function."""
        cache = CacheService()
        call_count = {"count": 0}

        def factory():
            call_count["count"] += 1
            return f"computed_value_{call_count['count']}"

        # First call should invoke factory
        result1 = cache.get_or_set("key", factory)
        assert result1 == "computed_value_1"
        assert call_count["count"] == 1

        # Second call should use cache
        result2 = cache.get_or_set("key", factory)
        assert result2 == "computed_value_1"
        assert call_count["count"] == 1  # Not called again


class TestCacheServiceStatistics:
    """Test cache statistics and monitoring."""

    def test_get_stats_returns_cache_statistics(self):
        """Test getting cache statistics."""
        cache = CacheService()
        cache.set("key1", "value1")
        cache.set("key2", "value2")

        stats = cache.get_stats()

        assert stats["size"] == 2
        assert stats["hits"] >= 0
        assert stats["misses"] >= 0
        assert "hit_rate" in stats

    def test_hit_miss_tracking(self):
        """Test that hits and misses are tracked."""
        cache = CacheService()
        cache.set("key", "value")

        # Hit
        cache.get("key")
        # Miss
        cache.get("nonexistent")

        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1

    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        cache = CacheService()
        cache.set("key", "value")

        cache.get("key")  # Hit
        cache.get("key")  # Hit
        cache.get("miss")  # Miss

        stats = cache.get_stats()
        assert stats["hit_rate"] == pytest.approx(0.666, abs=0.01)


class TestCacheServiceKeyGeneration:
    """Test cache key generation helpers."""

    def test_make_key_from_args(self):
        """Test generating cache key from arguments."""
        key1 = CacheService.make_key("prefix", "arg1", "arg2")
        key2 = CacheService.make_key("prefix", "arg1", "arg2")
        key3 = CacheService.make_key("prefix", "arg1", "different")

        assert key1 == key2  # Same args = same key
        assert key1 != key3  # Different args = different key

    def test_make_key_with_kwargs(self):
        """Test generating cache key with keyword arguments."""
        key1 = CacheService.make_key("prefix", param1="value1", param2="value2")
        key2 = CacheService.make_key("prefix", param1="value1", param2="value2")
        key3 = CacheService.make_key("prefix", param1="value1", param2="different")

        assert key1 == key2
        assert key1 != key3


class TestCacheServiceThreadSafety:
    """Test thread safety of cache operations."""

    def test_concurrent_sets_are_thread_safe(self):
        """Test that concurrent set operations are thread-safe."""
        import threading

        cache = CacheService()

        def set_values(thread_id):
            for i in range(100):
                cache.set(f"key_{thread_id}_{i}", f"value_{thread_id}_{i}")

        threads = [threading.Thread(target=set_values, args=(i,)) for i in range(5)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Should have 500 entries (5 threads * 100 each)
        assert cache.size() == 500


class TestCacheServiceInvalidation:
    """Test cache invalidation patterns."""

    def test_invalidate_by_prefix(self):
        """Test invalidating all keys with a prefix."""
        cache = CacheService()
        cache.set("user:1:profile", "data1")
        cache.set("user:1:settings", "data2")
        cache.set("user:2:profile", "data3")
        cache.set("post:1", "data4")

        cache.invalidate_prefix("user:1")

        assert cache.has("user:1:profile") is False
        assert cache.has("user:1:settings") is False
        assert cache.has("user:2:profile") is True
        assert cache.has("post:1") is True

    def test_invalidate_by_pattern(self):
        """Test invalidating keys matching a pattern."""
        cache = CacheService()
        cache.set("server:home:sessions", "data1")
        cache.set("server:work:sessions", "data2")
        cache.set("server:home:libraries", "data3")

        cache.invalidate_pattern("*:sessions")

        assert cache.has("server:home:sessions") is False
        assert cache.has("server:work:sessions") is False
        assert cache.has("server:home:libraries") is True
