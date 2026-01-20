"""
Unit tests for Memory Optimizer.

Tests the MemoryOptimizer utility and memory-related functions.
"""

import pytest

from plexiglass.utils.memory_optimizer import MemoryOptimizer


class TestMemoryOptimizerFormatting:
    """Test memory formatting functions."""

    def test_format_bytes_zero(self):
        """Test formatting 0 bytes."""
        result = MemoryOptimizer.format_bytes(0)
        assert "0.0 B" == result

    def test_format_bytes_kb(self):
        """Test formatting kilobytes."""
        result = MemoryOptimizer.format_bytes(1024)
        assert "KB" in result

    def test_format_bytes_mb(self):
        """Test formatting megabytes."""
        result = MemoryOptimizer.format_bytes(1024 * 1024)
        assert "MB" in result

    def test_format_bytes_gb(self):
        """Test formatting gigabytes."""
        result = MemoryOptimizer.format_bytes(1024 * 1024 * 1024)
        assert "GB" in result


class TestMemoryOptimizerGarbageCollection:
    """Test garbage collection functionality."""

    def test_force_garbage_collection_returns_dict(self):
        """Test that force_garbage_collection returns statistics."""
        result = MemoryOptimizer.force_garbage_collection()
        assert isinstance(result, dict)
        assert "collected" in result
        assert "generation_0" in result
        assert "generation_1" in result
        assert "generation_2" in result

    def test_force_garbage_collection_runs_all_generations(self):
        """Test that all 3 generations are collected."""
        result = MemoryOptimizer.force_garbage_collection()
        # All should be non-negative integers
        assert result["generation_0"] >= 0
        assert result["generation_1"] >= 0
        assert result["generation_2"] >= 0


class TestMemoryOptimizerStatus:
    """Test memory status reporting."""

    def test_get_memory_status_returns_string(self):
        """Test that get_memory_status returns a string."""
        result = MemoryOptimizer.get_memory_status()
        assert isinstance(result, str)

    def test_get_memory_status_contains_status_indicator(self):
        """Test that status contains OK/WARNING/CRITICAL."""
        result = MemoryOptimizer.get_memory_status()
        assert any(indicator in result for indicator in ["OK", "WARNING", "CRITICAL"])

    def test_get_memory_status_contains_size(self):
        """Test that status contains memory size."""
        result = MemoryOptimizer.get_memory_status()
        assert "MB" in result or "GB" in result or "KB" in result


class TestMemoryOptimizerSuggestions:
    """Test memory cleanup suggestions."""

    def test_suggest_cleanup_returns_list(self):
        """Test that suggest_cleanup returns a list."""
        suggestions = MemoryOptimizer.suggest_cleanup(cache_size=100, demo_count=5)
        assert isinstance(suggestions, list)

    def test_suggest_cleanup_large_cache(self):
        """Test suggestions when cache is large."""
        suggestions = MemoryOptimizer.suggest_cleanup(cache_size=1500, demo_count=5)
        assert len(suggestions) > 0

    def test_suggest_cleanup_many_demos(self):
        """Test suggestions when many demos are loaded."""
        suggestions = MemoryOptimizer.suggest_cleanup(cache_size=100, demo_count=25)
        assert len(suggestions) > 0
