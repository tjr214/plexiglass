"""
Integration tests for CategoryMenu widget.

Tests the CategoryMenu widget in a Textual app context.
"""

import pytest
from textual.app import App, ComposeResult

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry
from plexiglass.ui.widgets.category_menu import CategoryMenu


class SampleDemo(BaseDemo):
    """Sample demo for testing."""

    name = "Test Demo"
    description = "A test demo"
    category = "Server & Connection"
    operation_type = "read"

    def get_code_example(self, params=None):
        return "test()"

    def execute(self, server, params):
        return {"result": "test"}


class CategoryMenuApp(App):
    """Test app for CategoryMenu widget."""

    def __init__(self, registry: DemoRegistry):
        super().__init__()
        self.registry = registry
        self.messages = []

    def compose(self) -> ComposeResult:
        """Compose the app with CategoryMenu."""
        yield CategoryMenu(self.registry)

    def on_category_menu_category_selected(self, message: CategoryMenu.CategorySelected) -> None:
        """Handle category selection message."""
        self.messages.append(message)


@pytest.mark.asyncio
async def test_category_menu_renders_in_app():
    """Test CategoryMenu renders correctly in a Textual app."""
    registry = DemoRegistry()
    registry.register(SampleDemo)

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        # App should render successfully
        assert app is not None

        # CategoryMenu should be in the widget tree
        menu = app.query_one(CategoryMenu)
        assert menu is not None
        assert menu.registry is registry


@pytest.mark.asyncio
async def test_category_menu_displays_categories_in_app():
    """Test CategoryMenu displays categories in app context."""
    registry = DemoRegistry()

    class Demo1(BaseDemo):
        name = "Demo 1"
        description = "First demo"
        category = "Server & Connection"
        operation_type = "read"

        def get_code_example(self, params=None):
            return "demo1()"

        def execute(self, server, params):
            return {}

    class Demo2(BaseDemo):
        name = "Demo 2"
        description = "Second demo"
        category = "Library Management"
        operation_type = "read"

        def get_code_example(self, params=None):
            return "demo2()"

        def execute(self, server, params):
            return {}

    registry.register(Demo1)
    registry.register(Demo2)

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        menu = app.query_one(CategoryMenu)

        # Should have 2 categories
        categories = menu.get_categories()
        assert len(categories) == 2


@pytest.mark.asyncio
async def test_category_menu_handles_empty_registry_in_app():
    """Test CategoryMenu with empty registry in app context."""
    registry = DemoRegistry()

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        menu = app.query_one(CategoryMenu)

        # Should handle empty gracefully
        categories = menu.get_categories()
        assert categories == []


@pytest.mark.asyncio
async def test_category_menu_message_propagation():
    """Test CategorySelected message propagates to parent app."""
    registry = DemoRegistry()
    registry.register(SampleDemo)

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        menu = app.query_one(CategoryMenu)

        # Manually trigger category selection
        menu.select_category("Server & Connection")

        # Wait for message to propagate
        await pilot.pause()

        # App should have received the message
        assert len(app.messages) == 1
        assert app.messages[0].category == "Server & Connection"


@pytest.mark.asyncio
async def test_category_menu_composition_with_categories():
    """Test CategoryMenu composition includes ListView."""
    registry = DemoRegistry()
    registry.register(SampleDemo)

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        # Should have a ListView
        from textual.widgets import ListView

        list_view = app.query_one(ListView)
        assert list_view is not None


@pytest.mark.asyncio
async def test_category_menu_composition_without_categories():
    """Test CategoryMenu composition with empty registry shows message."""
    registry = DemoRegistry()

    app = CategoryMenuApp(registry)
    async with app.run_test() as pilot:
        from textual.widgets import Label

        # Should have a Label saying no categories
        label = app.query_one(Label)
        assert label is not None
        # Check the label text
        assert label.render() == "No categories available"
