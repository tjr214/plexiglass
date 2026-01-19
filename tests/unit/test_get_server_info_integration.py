"""
Integration tests for GetServerInfoDemo with DemoRegistry.

Tests that the demo properly integrates with the registry system.
"""

from __future__ import annotations

from plexiglass.gallery.demos.server.get_server_info import GetServerInfoDemo
from plexiglass.gallery.registry import DemoRegistry


class TestGetServerInfoDemoRegistration:
    """Test suite for GetServerInfoDemo registry integration."""

    def test_demo_can_be_registered(self) -> None:
        """Demo should be registerable with the registry."""
        registry = DemoRegistry()

        # Register the demo
        registry.register(GetServerInfoDemo)

        # Verify it's registered
        assert registry.get_demo_count() == 1
        all_demos = registry.get_all_demos()
        assert len(all_demos) == 1
        assert all_demos[0].name == "Get Server Info"

    def test_demo_appears_in_server_category(self) -> None:
        """Demo should appear in 'Server & Connection' category."""
        registry = DemoRegistry()
        registry.register(GetServerInfoDemo)

        # Get demos by category
        server_demos = registry.get_demos_by_category("Server & Connection")
        assert len(server_demos) == 1
        assert server_demos[0].name == "Get Server Info"

    def test_demo_can_be_found_by_name(self) -> None:
        """Demo should be findable by name."""
        registry = DemoRegistry()
        registry.register(GetServerInfoDemo)

        # Find by name
        demo = registry.get_demo_by_name("Get Server Info")
        assert demo is not None
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_registration_with_decorator(self) -> None:
        """Demo should be registerable using decorator syntax."""
        registry = DemoRegistry()

        # Use decorator syntax
        @registry.register_demo
        class TestDemo(GetServerInfoDemo):
            pass

        # Verify registration worked
        assert registry.get_demo_count() == 1

    def test_multiple_demos_in_same_category(self) -> None:
        """Registry should handle multiple demos in same category."""
        registry = DemoRegistry()

        # Register original demo
        registry.register(GetServerInfoDemo)

        # Create and register a second demo in same category
        @registry.register_demo
        class AnotherServerDemo(GetServerInfoDemo):
            name = "Another Server Demo"
            description = "Another test demo"

        # Verify both are registered
        assert registry.get_demo_count() == 2
        server_demos = registry.get_demos_by_category("Server & Connection")
        assert len(server_demos) == 2

    def test_category_appears_in_category_list(self) -> None:
        """Category should appear in all categories list."""
        registry = DemoRegistry()
        registry.register(GetServerInfoDemo)

        categories = registry.get_all_categories()
        assert "Server & Connection" in categories
