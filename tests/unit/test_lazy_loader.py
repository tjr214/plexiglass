"""
Unit tests for Lazy Loading functionality.

Tests the lazy loading system for gallery demos to prevent
instantiation of all demos at startup.
"""

from typing import Any

import pytest

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.lazy_loader import LazyDemoLoader


# Test demo classes
class TestDemo1(BaseDemo):
    """Test demo 1 for lazy loading."""

    name = "Test Demo 1"
    description = "A test demo"
    category = "Test Category"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return "# Example code"

    def execute(self, server, params: dict[str, Any]) -> dict[str, Any]:
        return {"result": "test"}


class TestDemo2(BaseDemo):
    """Test demo 2 for lazy loading."""

    name = "Test Demo 2"
    description = "Another test demo"
    category = "Test Category"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return "# Example code 2"

    def execute(self, server, params: dict[str, Any]) -> dict[str, Any]:
        return {"result": "test2"}


class TestLazyDemoLoaderInitialization:
    """Test LazyDemoLoader initialization."""

    def test_creates_loader_without_instantiating_demos(self):
        """Test that loader creates demo classes without instantiation."""
        loader = LazyDemoLoader()
        assert loader is not None

    def test_loader_starts_with_no_loaded_demos(self):
        """Test that no demos are loaded initially."""
        loader = LazyDemoLoader()
        assert loader.get_loaded_count() == 0


class TestLazyDemoLoaderRegistration:
    """Test demo registration in lazy loader."""

    def test_register_demo_class_without_instantiation(self):
        """Test registering a demo class doesn't instantiate it."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)

        # Demo should be registered but not loaded
        assert loader.get_registered_count() == 1
        assert loader.get_loaded_count() == 0

    def test_register_multiple_demo_classes(self):
        """Test registering multiple demo classes."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        assert loader.get_registered_count() == 2
        assert loader.get_loaded_count() == 0

    def test_decorator_registration(self):
        """Test using loader as a decorator."""
        loader = LazyDemoLoader()

        @loader.register_demo
        class DecoratorDemo(BaseDemo):
            name = "Decorator Demo"
            description = "Test"
            category = "Test"
            operation_type = "READ"

            def get_code_example(self, params: dict[str, Any] | None = None) -> str:
                return "# Test"

            def execute(self, server, params: dict[str, Any]) -> dict[str, Any]:
                return {}

        assert loader.get_registered_count() == 1
        assert loader.get_loaded_count() == 0


class TestLazyDemoLoaderLoading:
    """Test lazy loading mechanism."""

    def test_get_demo_loads_on_demand(self):
        """Test that accessing a demo loads it only when needed."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)

        # Demo not loaded yet
        assert loader.get_loaded_count() == 0

        # Accessing demo should load it
        demo = loader.get_demo("Test Demo 1")
        assert demo is not None
        assert loader.get_loaded_count() == 1

    def test_get_demo_reuses_loaded_instance(self):
        """Test that subsequent accesses return same instance."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)

        demo1 = loader.get_demo("Test Demo 1")
        demo2 = loader.get_demo("Test Demo 1")

        assert demo1 is demo2  # Same instance
        assert loader.get_loaded_count() == 1  # Still only loaded once

    def test_get_all_demos_loads_all(self):
        """Test that getting all demos loads all registered demos."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        assert loader.get_loaded_count() == 0

        all_demos = loader.get_all_demos()

        assert len(all_demos) == 2
        assert loader.get_loaded_count() == 2

    def test_get_demos_by_category_loads_only_category(self):
        """Test that filtering by category loads only matching demos."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        category_demos = loader.get_demos_by_category("Test Category")

        assert len(category_demos) == 2
        assert loader.get_loaded_count() == 2

    def test_get_demo_by_name_loads_specific_demo(self):
        """Test that getting by name loads only that demo."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        demo = loader.get_demo_by_name("Test Demo 1")

        assert demo is not None
        assert demo.name == "Test Demo 1"
        assert loader.get_loaded_count() == 1  # Only one loaded


class TestLazyDemoLoaderQuerying:
    """Test querying demo metadata without loading."""

    def test_get_all_categories_without_loading(self):
        """Test getting categories doesn't load demos."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        categories = loader.get_all_categories()

        assert "Test Category" in categories
        assert loader.get_loaded_count() == 0  # No demos loaded

    def test_get_demo_count_without_loading(self):
        """Test getting count doesn't load demos."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        count = loader.get_demo_count()

        assert count == 2
        assert loader.get_loaded_count() == 0

    def test_get_category_count_without_loading(self):
        """Test getting category count doesn't load demos."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        count = loader.get_category_count("Test Category")

        assert count == 2
        assert loader.get_loaded_count() == 0


class TestLazyDemoLoaderClearing:
    """Test clearing loaded demos."""

    def test_clear_loaded_demos(self):
        """Test clearing loaded demos while keeping registrations."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        # Load demos
        _ = loader.get_all_demos()
        assert loader.get_loaded_count() == 2

        # Clear loaded
        loader.clear_loaded()

        assert loader.get_loaded_count() == 0
        assert loader.get_registered_count() == 2

    def test_clear_all_clears_registrations_and_loaded(self):
        """Test clearing everything."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)

        _ = loader.get_all_demos()
        assert loader.get_loaded_count() == 1

        loader.clear_all()

        assert loader.get_loaded_count() == 0
        assert loader.get_registered_count() == 0


class TestLazyDemoLoaderStatistics:
    """Test statistics tracking."""

    def test_get_statistics(self):
        """Test getting loader statistics."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        stats = loader.get_statistics()

        assert stats["registered"] == 2
        assert stats["loaded"] == 0
        assert "load_percentage" in stats

    def test_statistics_update_after_loading(self):
        """Test that statistics update after loading."""
        loader = LazyDemoLoader()
        loader.register(TestDemo1)
        loader.register(TestDemo2)

        _ = loader.get_demo("Test Demo 1")

        stats = loader.get_statistics()
        assert stats["registered"] == 2
        assert stats["loaded"] == 1
        assert stats["load_percentage"] == pytest.approx(50.0)
