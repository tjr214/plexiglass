"""
Tests for the DemoRegistry class.

The DemoRegistry manages registration and discovery of gallery demos.
"""

from __future__ import annotations

import pytest

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


class TestDemoRegistry:
    """Test suite for DemoRegistry class."""

    def test_registry_initializes_empty(self) -> None:
        """Registry should initialize with no demos registered."""
        registry = DemoRegistry()
        assert registry.get_all_demos() == []

    def test_registry_can_register_demo(self) -> None:
        """Registry should allow registering a demo class."""

        class SampleDemo(BaseDemo):
            name = "Sample Demo"
            description = "A sample demonstration"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        registry.register(SampleDemo)
        demos = registry.get_all_demos()
        assert len(demos) == 1
        assert isinstance(demos[0], SampleDemo)

    def test_registry_get_demos_by_category(self) -> None:
        """Registry should filter demos by category."""

        class ServerDemo(BaseDemo):
            name = "Server Demo"
            description = "Server demo"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class LibraryDemo(BaseDemo):
            name = "Library Demo"
            description = "Library demo"
            category = "Library Management"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        registry.register(ServerDemo)
        registry.register(LibraryDemo)

        server_demos = registry.get_demos_by_category("Server & Connection")
        assert len(server_demos) == 1
        assert isinstance(server_demos[0], ServerDemo)

        library_demos = registry.get_demos_by_category("Library Management")
        assert len(library_demos) == 1
        assert isinstance(library_demos[0], LibraryDemo)

    def test_registry_get_all_categories(self) -> None:
        """Registry should return list of all categories with registered demos."""

        class Demo1(BaseDemo):
            name = "Demo 1"
            description = "Demo 1"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class Demo2(BaseDemo):
            name = "Demo 2"
            description = "Demo 2"
            category = "Library Management"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class Demo3(BaseDemo):
            name = "Demo 3"
            description = "Demo 3"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        registry.register(Demo1)
        registry.register(Demo2)
        registry.register(Demo3)

        categories = registry.get_all_categories()
        assert len(categories) == 2
        assert "Server & Connection" in categories
        assert "Library Management" in categories

    def test_registry_get_demo_by_name(self) -> None:
        """Registry should find a demo by its name."""

        class TargetDemo(BaseDemo):
            name = "Target Demo"
            description = "The demo we want"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        registry.register(TargetDemo)

        demo = registry.get_demo_by_name("Target Demo")
        assert demo is not None
        assert isinstance(demo, TargetDemo)

    def test_registry_get_demo_by_name_returns_none_if_not_found(self) -> None:
        """Registry should return None if demo name not found."""
        registry = DemoRegistry()
        demo = registry.get_demo_by_name("Nonexistent")
        assert demo is None

    def test_registry_get_demo_count(self) -> None:
        """Registry should return count of registered demos."""

        class Demo1(BaseDemo):
            name = "Demo 1"
            description = "Demo 1"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class Demo2(BaseDemo):
            name = "Demo 2"
            description = "Demo 2"
            category = "Library Management"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        assert registry.get_demo_count() == 0

        registry.register(Demo1)
        assert registry.get_demo_count() == 1

        registry.register(Demo2)
        assert registry.get_demo_count() == 2

    def test_registry_get_category_count(self) -> None:
        """Registry should return count of demos in a category."""

        class Demo1(BaseDemo):
            name = "Demo 1"
            description = "Demo 1"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class Demo2(BaseDemo):
            name = "Demo 2"
            description = "Demo 2"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        class Demo3(BaseDemo):
            name = "Demo 3"
            description = "Demo 3"
            category = "Library Management"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        registry = DemoRegistry()
        registry.register(Demo1)
        registry.register(Demo2)
        registry.register(Demo3)

        assert registry.get_category_count("Server & Connection") == 2
        assert registry.get_category_count("Library Management") == 1
        assert registry.get_category_count("Nonexistent") == 0

    def test_registry_can_use_decorator(self) -> None:
        """Registry should support @register_demo decorator."""
        registry = DemoRegistry()

        @registry.register_demo
        class DecoratedDemo(BaseDemo):
            name = "Decorated Demo"
            description = "Registered via decorator"
            category = "Server & Connection"
            operation_type = "READ"

            def execute(self, server, params):
                return {}

        demos = registry.get_all_demos()
        assert len(demos) == 1
        assert isinstance(demos[0], DecoratedDemo)
