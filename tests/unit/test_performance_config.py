"""
Unit tests for Performance Configuration.

Tests the PerformanceConfig module and optimization settings.
"""

import pytest

from plexiglass.config.performance import PerformanceConfig


class TestPerformanceConfigDefaults:
    """Test default performance settings."""

    def test_get_defaults_returns_dict(self):
        """Test that get_defaults returns a dictionary."""
        defaults = PerformanceConfig.get_defaults()
        assert isinstance(defaults, dict)

    def test_defaults_have_worker_threads(self):
        """Test that defaults include worker_threads setting."""
        defaults = PerformanceConfig.get_defaults()
        assert "worker_threads" in defaults
        assert defaults["worker_threads"] == PerformanceConfig.DEFAULT_WORKER_THREADS

    def test_defaults_have_cache_settings(self):
        """Test that defaults include cache settings."""
        defaults = PerformanceConfig.get_defaults()
        assert "cache_ttl" in defaults
        assert "cache_size" in defaults

    def test_defaults_have_connection_settings(self):
        """Test that defaults include connection settings."""
        defaults = PerformanceConfig.get_defaults()
        assert "connection_timeout" in defaults
        assert "pool_max_size" in defaults

    def test_defaults_have_cache_ttls(self):
        """Test that defaults include cache-specific TTLs."""
        defaults = PerformanceConfig.get_defaults()
        assert "cache_ttls" in defaults
        ttl_dict = defaults["cache_ttls"]
        assert "server_info" in ttl_dict
        assert "library_list" in ttl_dict
        assert "sessions" in ttl_dict

    def test_defaults_have_worker_pools(self):
        """Test that defaults include worker pool settings."""
        defaults = PerformanceConfig.get_defaults()
        assert "worker_pools" in defaults
        pool_dict = defaults["worker_pools"]
        assert "gallery_demo" in pool_dict
        assert "dashboard_refresh" in pool_dict


class TestPerformanceConfigMerging:
    """Test merging user settings with defaults."""

    def test_merge_with_none_returns_defaults(self):
        """Test that merging with None returns defaults."""
        settings = PerformanceConfig.get_optimized_settings(None)
        defaults = PerformanceConfig.get_defaults()
        assert settings == defaults

    def test_merge_with_empty_dict_returns_defaults(self):
        """Test that merging with empty dict returns defaults."""
        settings = PerformanceConfig.get_optimized_settings({})
        defaults = PerformanceConfig.get_defaults()
        assert settings == defaults

    def test_merge_overrides_top_level_settings(self):
        """Test that user settings override defaults."""
        user_settings = {"performance": {"worker_threads": 8}}
        settings = PerformanceConfig.get_optimized_settings(user_settings)

        assert settings["worker_threads"] == 8

    def test_merge_preserves_non_overridden_settings(self):
        """Test that non-overridden settings are preserved."""
        user_settings = {"performance": {"worker_threads": 8}}
        settings = PerformanceConfig.get_optimized_settings(user_settings)

        # Should preserve default values for other settings
        assert settings["cache_ttl"] == PerformanceConfig.DEFAULT_CACHE_TTL

    def test_merge_deep_merges_nested_dicts(self):
        """Test that nested dicts are merged deeply."""
        user_settings = {"performance": {"cache_ttls": {"server_info": 999}}}
        settings = PerformanceConfig.get_optimized_settings(user_settings)

        # Should override server_info but preserve other TTLs
        assert settings["cache_ttls"]["server_info"] == 999
        assert settings["cache_ttls"]["library_list"] == PerformanceConfig.LIBRARY_LIST_CACHE_TTL


class TestPerformanceConfigValidation:
    """Test performance settings validation."""

    def test_validate_valid_settings_returns_empty(self):
        """Test that valid settings pass validation."""
        settings = PerformanceConfig.get_defaults()
        errors = PerformanceConfig.validate_settings(settings)
        assert errors == []

    def test_validate_low_worker_threads(self):
        """Test that worker_threads < 1 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["worker_threads"] = 0
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("worker_threads" in e for e in errors)

    def test_validate_high_worker_threads(self):
        """Test that worker_threads > 16 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["worker_threads"] = 20
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("worker_threads" in e for e in errors)

    def test_validate_low_cache_ttl(self):
        """Test that cache_ttl < 1 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["cache_ttl"] = 0
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("cache_ttl" in e for e in errors)

    def test_validate_high_cache_ttl(self):
        """Test that cache_ttl > 3600 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["cache_ttl"] = 5000
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("cache_ttl" in e for e in errors)

    def test_validate_low_cache_size(self):
        """Test that cache_size < 10 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["cache_size"] = 5
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("cache_size" in e for e in errors)

    def test_validate_high_cache_size(self):
        """Test that cache_size > 10000 fails validation."""
        settings = PerformanceConfig.get_defaults()
        settings["cache_size"] = 15000
        errors = PerformanceConfig.validate_settings(settings)

        assert len(errors) > 0
        assert any("cache_size" in e for e in errors)

    def test_validate_connection_timeout(self):
        """Test that connection timeout bounds are enforced."""
        settings = PerformanceConfig.get_defaults()

        # Too low
        settings["connection_timeout"] = 2
        errors_low = PerformanceConfig.validate_settings(settings)
        assert len(errors_low) > 0

        # Too high
        settings["connection_timeout"] = 150
        errors_high = PerformanceConfig.validate_settings(settings)
        assert len(errors_high) > 0
