"""
Tests for CategoryMenu widget.

The CategoryMenu provides interactive navigation through gallery demo categories.
"""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import ListView, ListItem, Label

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry
from plexiglass.ui.widgets.category_menu import CategoryMenu


class SampleDemo1(BaseDemo):
    """Sample demo for Server category."""

    name = "Server Info Demo"
    description = "Get server information"
    category = "Server & Connection"
    operation_type = "read"

    def get_code_example(self, params=None):
        return "plex.version()"

    def execute(self, server, params):
        return {"result": "sample"}


class SampleDemo2(BaseDemo):
    """Sample demo for Library category."""

    name = "Library List Demo"
    description = "List all libraries"
    category = "Library Management"
    operation_type = "read"

    def get_code_example(self, params=None):
        return "plex.library.sections()"

    def execute(self, server, params):
        return {"result": "sample"}


class SampleDemo3(BaseDemo):
    """Another demo for Server category."""

    name = "Server Sessions Demo"
    description = "Get active sessions"
    category = "Server & Connection"
    operation_type = "read"

    def get_code_example(self, params=None):
        return "plex.sessions()"

    def execute(self, server, params):
        return {"result": "sample"}


class TestCategoryMenu:
    """Test suite for CategoryMenu widget."""

    def test_category_menu_initialization_with_empty_registry(self):
        """Test CategoryMenu initializes with empty registry."""
        registry = DemoRegistry()
        menu = CategoryMenu(registry)

        assert menu.registry is registry
        assert menu.selected_category is None

    def test_category_menu_initialization_with_populated_registry(self):
        """Test CategoryMenu initializes with populated registry."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)
        registry.register(SampleDemo2)

        menu = CategoryMenu(registry)

        assert menu.registry is registry
        assert len(registry.get_all_categories()) == 2

    def test_category_menu_displays_all_categories(self):
        """Test CategoryMenu displays all available categories."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)
        registry.register(SampleDemo2)
        registry.register(SampleDemo3)

        menu = CategoryMenu(registry)
        categories = menu.get_categories()

        assert len(categories) == 2
        assert "Server & Connection" in categories
        assert "Library Management" in categories

    def test_category_menu_shows_demo_count_per_category(self):
        """Test CategoryMenu shows demo count for each category."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)  # Server & Connection
        registry.register(SampleDemo2)  # Library Management
        registry.register(SampleDemo3)  # Server & Connection

        menu = CategoryMenu(registry)

        # Should show counts: Server & Connection (2), Library Management (1)
        server_count = registry.get_category_count("Server & Connection")
        library_count = registry.get_category_count("Library Management")

        assert server_count == 2
        assert library_count == 1

    def test_category_menu_selection_changes_selected_category(self):
        """Test selecting a category updates the selected_category property."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)
        registry.register(SampleDemo2)

        menu = CategoryMenu(registry)

        # Initially no selection
        assert menu.selected_category is None

        # Simulate selection
        menu.select_category("Server & Connection")
        assert menu.selected_category == "Server & Connection"

        # Change selection
        menu.select_category("Library Management")
        assert menu.selected_category == "Library Management"

    def test_category_menu_emits_message_on_selection(self):
        """Test CategoryMenu emits CategorySelected message when category is selected."""
        # This will test the custom message system
        registry = DemoRegistry()
        registry.register(SampleDemo1)

        menu = CategoryMenu(registry)

        # Verify the CategorySelected message class exists
        assert hasattr(CategoryMenu, "CategorySelected")

    def test_category_menu_handles_empty_categories_gracefully(self):
        """Test CategoryMenu handles empty registry gracefully."""
        registry = DemoRegistry()
        menu = CategoryMenu(registry)

        categories = menu.get_categories()
        assert categories == []
        assert menu.selected_category is None

    def test_category_menu_get_category_emoji(self):
        """Test CategoryMenu provides emoji icons for categories."""
        registry = DemoRegistry()
        menu = CategoryMenu(registry)

        # Should have emoji mapping
        emoji = menu.get_category_emoji("Server & Connection")
        assert emoji is not None
        assert isinstance(emoji, str)

    def test_category_menu_formats_category_display(self):
        """Test CategoryMenu formats category display with emoji and count."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)
        registry.register(SampleDemo3)

        menu = CategoryMenu(registry)

        # Should format as: "📡 Server & Connection (2)"
        display = menu.format_category_display("Server & Connection")
        assert "Server & Connection" in display
        assert "(2)" in display  # Demo count

    def test_category_menu_composes_list_items(self):
        """Test CategoryMenu composes ListItems for each category."""
        registry = DemoRegistry()
        registry.register(SampleDemo1)
        registry.register(SampleDemo2)

        menu = CategoryMenu(registry)

        # Should compose a ListView with ListItems
        # This will be tested in integration, but we verify the structure
        assert hasattr(menu, "compose")

    def test_category_menu_handles_category_with_special_characters(self):
        """Test CategoryMenu handles category names with special characters."""
        registry = DemoRegistry()

        class SpecialCategoryDemo(BaseDemo):
            name = "Special Demo"
            description = "Test demo"
            category = "Users & Sharing"  # Has ampersand
            operation_type = "read"

            def get_code_example(self, params=None):
                return "plex.users()"

            def execute(self, server, params):
                return {"result": "sample"}

        registry.register(SpecialCategoryDemo)
        menu = CategoryMenu(registry)

        categories = menu.get_categories()
        assert "Users & Sharing" in categories

    def test_category_menu_sorts_categories_alphabetically(self):
        """Test CategoryMenu sorts categories alphabetically."""
        registry = DemoRegistry()

        # Register demos in non-alphabetical order
        class ZDemo(BaseDemo):
            name = "Z Demo"
            description = "Z"
            category = "Utilities"
            operation_type = "read"

            def get_code_example(self, params=None):
                return "z"

            def execute(self, server, params):
                return {}

        class ADemo(BaseDemo):
            name = "A Demo"
            description = "A"
            category = "Advanced Features"
            operation_type = "read"

            def get_code_example(self, params=None):
                return "a"

            def execute(self, server, params):
                return {}

        registry.register(ZDemo)
        registry.register(ADemo)

        menu = CategoryMenu(registry)
        categories = menu.get_categories()

        # Should be sorted: Advanced Features, Utilities
        assert categories == ["Advanced Features", "Utilities"]
