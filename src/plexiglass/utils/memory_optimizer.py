"""
Memory Optimization Utilities for PlexiGlass.

Provides memory-efficient patterns and cleanup strategies.
"""

import gc
import sys
from typing import Any


class MemoryOptimizer:
    """
    Memory optimization utilities and patterns.

    Provides methods for:
    - Memory usage monitoring
    - Garbage collection hints
    - Cache cleanup strategies
    - Memory profile helpers
    """

    # Memory size thresholds (in bytes)
    WARNING_THRESHOLD = 100 * 1024 * 1024  # 100 MB
    CRITICAL_THRESHOLD = 200 * 1024 * 1024  # 200 MB

    @staticmethod
    def get_memory_usage() -> dict[str, int]:
        """
        Get current memory usage statistics.

        Returns:
            Dictionary with memory statistics:
            - current: Current memory usage in bytes
            - peak: Peak memory usage in bytes
            - system_total: Total system memory in bytes
            - system_available: Available system memory in bytes
        """
        # Initialize default values
        system_total = 0
        system_available = 0

        # Try to get memory usage from resource module (Unix-like systems)
        try:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            current = usage.ru_maxrss * 1024  # Convert KB to bytes

            # Get system memory
            try:
                with open("/proc/meminfo", "r") as f:
                    meminfo = f.read()
                    for line in meminfo.split("\n"):
                        if line.startswith("MemTotal:"):
                            system_total = int(line.split()[1]) * 1024
                        if line.startswith("MemAvailable:"):
                            system_available = int(line.split()[1]) * 1024
            except (FileNotFoundError, IOError, ValueError):
                system_total = 0
                system_available = 0

            return {
                "current": current,
                "peak": current,
                "system_total": system_total,
                "system_available": system_available,
            }
        except ImportError:
            # Fallback: estimate from sys module
            import sys

            return {
                "current": sys.getsizeof([]),  # Rough estimate
                "peak": sys.getsizeof([]),
                "system_total": 0,
                "system_available": 0,
            }

    @staticmethod
    def format_bytes(size_bytes: int | float) -> str:
        """
        Format bytes to human-readable string.

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted string (e.g., "1.5 MB")
        """
        size_float = float(size_bytes)
        for unit in ["B", "KB", "MB", "GB"]:
            if size_float < 1024:
                return f"{size_float:.1f} {unit}"
            size_float /= 1024
        return f"{size_float:.1f} TB"

    @staticmethod
    def force_garbage_collection() -> dict[str, Any]:
        """
        Force garbage collection to free memory.

        Returns:
            Dictionary with collection statistics:
            - collected: Number of objects collected
            - uncollectable: Number of uncollectable objects
            - generation_0: Objects collected in generation 0
            - generation_1: Objects collected in generation 1
            - generation_2: Objects collected in generation 2
        """
        # Run all 3 generations of garbage collection
        collected = gc.collect()

        return {
            "collected": collected,
            "uncollectable": len(gc.garbage),
            "generation_0": gc.collect(0),
            "generation_1": gc.collect(1),
            "generation_2": gc.collect(2),
        }

    @staticmethod
    def get_memory_status() -> str:
        """
        Get current memory status as a human-readable string.

        Returns:
            Memory status string (e.g., "OK (45.2 MB)")
        """
        usage = MemoryOptimizer.get_memory_usage()
        current = usage["current"]

        if current >= MemoryOptimizer.CRITICAL_THRESHOLD:
            status = "CRITICAL"
        elif current >= MemoryOptimizer.WARNING_THRESHOLD:
            status = "WARNING"
        else:
            status = "OK"

        formatted = MemoryOptimizer.format_bytes(current)
        return f"{status} ({formatted})"

    @staticmethod
    def suggest_cleanup(cache_size: int, demo_count: int) -> list[str]:
        """
        Suggest memory cleanup actions based on current state.

        Args:
            cache_size: Current number of cached entries
            demo_count: Number of loaded demos

        Returns:
            List of suggested cleanup actions
        """
        suggestions = []

        # Cache size suggestions
        if cache_size > 1000:
            suggestions.append(
                f"Large cache detected ({cache_size} entries). "
                "Consider reducing cache_ttl or cache_size settings."
            )

        # Demo count suggestions
        if demo_count > 20:
            suggestions.append(
                f"Many demos loaded ({demo_count}). Consider using lazy loading to free memory."
            )

        # Memory usage suggestions
        usage = MemoryOptimizer.get_memory_usage()
        if usage["current"] >= MemoryOptimizer.WARNING_THRESHOLD:
            suggestions.append(
                "Memory usage high. Consider running garbage collection or reducing cache sizes."
            )

        if not suggestions:
            suggestions.append("Memory usage looks healthy!")

        return suggestions

    @staticmethod
    def optimize_imports() -> None:
        """
        Optimize import patterns for memory efficiency.

        Lazy imports help reduce memory footprint by only loading
        modules when they're actually used.
        """
        # This is documentation only - actual optimization
        # should be done at the module level
        pass

    @staticmethod
    def check_for_memory_leaks(threshold: int = 5) -> bool:
        """
        Check for potential memory leaks.

        Simple heuristic: if memory usage is consistently high
        across multiple garbage collections, there may be a leak.

        Args:
            threshold: Number of collections to check

        Returns:
            True if potential leak detected, False otherwise
        """
        # This is a simplified check - real leak detection
        # would require more sophisticated profiling
        usage = MemoryOptimizer.get_memory_usage()
        return usage["current"] >= MemoryOptimizer.CRITICAL_THRESHOLD
