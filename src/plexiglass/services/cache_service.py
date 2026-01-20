"""
Cache Service for PlexiGlass.

Provides request caching with TTL (Time-To-Live) support for improved performance.
"""

import hashlib
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Optional
from fnmatch import fnmatch


class CacheEntry:
    """Represents a single cache entry with expiration."""

    def __init__(self, value: Any, ttl: int):
        """
        Initialize a cache entry.

        Args:
            value: The cached value
            ttl: Time-to-live in seconds
        """
        self.value = value
        self.expiry = datetime.now() + timedelta(seconds=ttl)
        self.created_at = datetime.now()

    def is_expired(self) -> bool:
        """Check if this cache entry has expired."""
        return datetime.now() >= self.expiry


class CacheService:
    """
    Thread-safe caching service with TTL support.

    Features:
    - TTL-based expiration
    - Thread-safe operations
    - Hit/miss statistics
    - Pattern-based invalidation
    - Key generation helpers

    Example:
        >>> cache = CacheService(default_ttl=60)
        >>> cache.set("user:1", {"name": "John"})
        >>> user = cache.get("user:1")
        >>> print(user)
        {'name': 'John'}
    """

    def __init__(self, default_ttl: int = 60):
        """
        Initialize the cache service.

        Args:
            default_ttl: Default time-to-live in seconds (default: 60)
        """
        self.default_ttl = default_ttl
        self._cache: dict[str, CacheEntry] = {}
        self._lock = threading.RLock()
        self._hits = 0
        self._misses = 0

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional custom TTL in seconds (uses default if not provided)
        """
        with self._lock:
            ttl_to_use = ttl if ttl is not None else self.default_ttl
            self._cache[key] = CacheEntry(value, ttl_to_use)

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Cached value if exists and not expired, None otherwise
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            entry = self._cache[key]
            if entry.is_expired():
                # Clean up expired entry
                del self._cache[key]
                self._misses += 1
                return None

            self._hits += 1
            return entry.value

    def has(self, key: str) -> bool:
        """
        Check if a key exists in the cache and is not expired.

        Args:
            key: Cache key

        Returns:
            True if key exists and not expired, False otherwise
        """
        with self._lock:
            if key not in self._cache:
                return False

            entry = self._cache[key]
            if entry.is_expired():
                # Clean up expired entry
                del self._cache[key]
                return False

            return True

    def delete(self, key: str) -> None:
        """
        Delete a key from the cache.

        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    def size(self) -> int:
        """
        Get the number of valid (non-expired) entries in the cache.

        Returns:
            Number of cache entries
        """
        with self._lock:
            # Clean up expired entries
            self._cleanup_expired()
            return len(self._cache)

    def is_empty(self) -> bool:
        """
        Check if the cache is empty.

        Returns:
            True if cache has no valid entries, False otherwise
        """
        return self.size() == 0

    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: Optional[int] = None) -> Any:
        """
        Get a value from cache, or compute and cache it if not present.

        Args:
            key: Cache key
            factory: Function to compute value if not cached
            ttl: Optional custom TTL in seconds

        Returns:
            Cached or computed value
        """
        value = self.get(key)
        if value is not None:
            return value

        # Compute and cache
        computed_value = factory()
        self.set(key, computed_value, ttl)
        return computed_value

    def get_stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics:
            - size: Number of entries
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_rate: Cache hit rate (0.0 to 1.0)
        """
        with self._lock:
            self._cleanup_expired()
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

            return {
                "size": len(self._cache),
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
            }

    def invalidate_prefix(self, prefix: str) -> None:
        """
        Invalidate all cache entries with keys starting with the given prefix.

        Args:
            prefix: Key prefix to match
        """
        with self._lock:
            keys_to_delete = [key for key in self._cache.keys() if key.startswith(prefix)]
            for key in keys_to_delete:
                del self._cache[key]

    def invalidate_pattern(self, pattern: str) -> None:
        """
        Invalidate all cache entries with keys matching the given pattern.

        Supports glob-style patterns (*, ?, []).

        Args:
            pattern: Pattern to match (e.g., "user:*:sessions")
        """
        with self._lock:
            keys_to_delete = [key for key in self._cache.keys() if fnmatch(key, pattern)]
            for key in keys_to_delete:
                del self._cache[key]

    def _cleanup_expired(self) -> None:
        """Remove all expired entries from the cache (internal use)."""
        keys_to_delete = [key for key, entry in self._cache.items() if entry.is_expired()]
        for key in keys_to_delete:
            del self._cache[key]

    @staticmethod
    def make_key(*args: Any, **kwargs: Any) -> str:
        """
        Generate a cache key from arguments.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key as a string
        """
        # Create a deterministic representation
        parts = list(args)

        # Add sorted kwargs for consistency
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            parts.append(tuple(sorted_kwargs))

        # Convert to JSON for hashing
        key_data = json.dumps(parts, sort_keys=True, default=str)

        # Hash to keep keys reasonably sized
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]
