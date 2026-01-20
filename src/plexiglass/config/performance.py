"""
Performance Configuration for PlexiGlass.

Provides centralized performance settings for async operations,
worker pools, caching, and memory management.
"""

from typing import Any


class PerformanceConfig:
    """
    Centralized performance configuration for PlexiGlass.

    Provides tunable settings for:
    - Async worker pools
    - Cache sizes and TTLs
    - Connection timeouts
    - Memory limits
    - Refresh intervals

    Settings can be overridden via user configuration file.
    """

    # Default values
    DEFAULT_WORKER_THREADS = 4
    DEFAULT_CACHE_TTL = 60  # seconds
    DEFAULT_CACHE_SIZE = 1000  # max entries
    DEFAULT_CONNECTION_TIMEOUT = 30  # seconds
    DEFAULT_REFRESH_INTERVAL = 5  # seconds
    DEFAULT_POOL_MAX_SIZE = 10  # connections
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_MEMORY_CLEANUP_INTERVAL = 300  # seconds (5 minutes)

    # Cache-specific defaults
    SERVER_INFO_CACHE_TTL = 120  # 2 minutes - server info changes infrequently
    LIBRARY_LIST_CACHE_TTL = 300  # 5 minutes - library lists change infrequently
    SESSION_LIST_CACHE_TTL = 10  # 10 seconds - sessions change frequently
    DEMO_CODE_CACHE_TTL = 3600  # 1 hour - code examples never change

    # Worker pool defaults
    GALLERY_DEMO_WORKER_THREADS = 2  # Separate pool for demo execution
    DASHBOARD_REFRESH_WORKER_THREADS = 1  # Single thread for dashboard refreshes

    @staticmethod
    def get_defaults() -> dict[str, Any]:
        """
        Get all default performance settings.

        Returns:
            Dictionary of default performance settings
        """
        return {
            "worker_threads": PerformanceConfig.DEFAULT_WORKER_THREADS,
            "cache_ttl": PerformanceConfig.DEFAULT_CACHE_TTL,
            "cache_size": PerformanceConfig.DEFAULT_CACHE_SIZE,
            "connection_timeout": PerformanceConfig.DEFAULT_CONNECTION_TIMEOUT,
            "refresh_interval": PerformanceConfig.DEFAULT_REFRESH_INTERVAL,
            "pool_max_size": PerformanceConfig.DEFAULT_POOL_MAX_SIZE,
            "max_retries": PerformanceConfig.DEFAULT_MAX_RETRIES,
            "memory_cleanup_interval": PerformanceConfig.DEFAULT_MEMORY_CLEANUP_INTERVAL,
            # Cache-specific TTLs
            "cache_ttls": {
                "server_info": PerformanceConfig.SERVER_INFO_CACHE_TTL,
                "library_list": PerformanceConfig.LIBRARY_LIST_CACHE_TTL,
                "sessions": PerformanceConfig.SESSION_LIST_CACHE_TTL,
                "demo_code": PerformanceConfig.DEMO_CODE_CACHE_TTL,
            },
            # Worker pool sizes
            "worker_pools": {
                "gallery_demo": PerformanceConfig.GALLERY_DEMO_WORKER_THREADS,
                "dashboard_refresh": PerformanceConfig.DASHBOARD_REFRESH_WORKER_THREADS,
            },
        }

    @staticmethod
    def get_optimized_settings(user_settings: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Get performance settings, merging user overrides with defaults.

        Args:
            user_settings: Optional user-provided performance settings

        Returns:
            Merged performance settings
        """
        defaults = PerformanceConfig.get_defaults()

        if not user_settings:
            return defaults

        # Deep merge user settings
        performance_section = user_settings.get("performance", {})

        merged = defaults.copy()
        for key, value in performance_section.items():
            if key in merged:
                if isinstance(value, dict) and isinstance(merged[key], dict):
                    # Merge nested dicts
                    merged[key] = {**merged[key], **value}
                else:
                    merged[key] = value

        return merged

    @staticmethod
    def validate_settings(settings: dict[str, Any]) -> list[str]:
        """
        Validate performance settings.

        Args:
            settings: Settings dictionary to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate worker threads
        if settings.get("worker_threads", 0) < 1:
            errors.append("worker_threads must be at least 1")
        if settings.get("worker_threads", 0) > 16:
            errors.append("worker_threads should not exceed 16")

        # Validate cache settings
        if settings.get("cache_ttl", 0) < 1:
            errors.append("cache_ttl must be at least 1 second")
        if settings.get("cache_ttl", 0) > 3600:
            errors.append("cache_ttl should not exceed 3600 seconds (1 hour)")

        if settings.get("cache_size", 0) < 10:
            errors.append("cache_size must be at least 10 entries")
        if settings.get("cache_size", 0) > 10000:
            errors.append("cache_size should not exceed 10000 entries")

        # Validate connection settings
        if settings.get("connection_timeout", 0) < 5:
            errors.append("connection_timeout must be at least 5 seconds")
        if settings.get("connection_timeout", 0) > 120:
            errors.append("connection_timeout should not exceed 120 seconds")

        # Validate refresh interval
        if settings.get("refresh_interval", 0) < 1:
            errors.append("refresh_interval must be at least 1 second")
        if settings.get("refresh_interval", 0) > 60:
            errors.append("refresh_interval should not exceed 60 seconds")

        return errors
