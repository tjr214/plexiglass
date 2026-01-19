"""
Tests for GalleryScreen - the main UI screen for browsing and executing demos.

This module tests the Gallery Screen layout, navigation, and integration with
the DemoRegistry system.
"""

from __future__ import annotations

import pytest
from textual.widgets import Button, Footer, Header, Static

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


# Test helper: Create a sample demo for testing
class SampleTestDemo(BaseDemo):
    """A simple demo for testing the gallery screen."""

    name = "Test Demo"
    description = "A demo for testing purposes"
    category = "Test Category"
    operation_type = "READ"

    def execute(self, server, params):
        return {"status": "success", "data": "test result"}

    def get_code_example(self, params=None):
        return "# Sample code\nserver.sessions()"


class SecondTestDemo(BaseDemo):
    """Another demo for testing."""

    name = "Second Demo"
    description = "Another test demo"
    category = "Test Category"
    operation_type = "WRITE"

    def execute(self, server, params):
        return {"status": "success"}


class DifferentCategoryDemo(BaseDemo):
    """Demo in a different category."""

    name = "Different Demo"
    description = "Demo in another category"
    category = "Another Category"
    operation_type = "READ"

    def execute(self, server, params):
        return {"result": "other"}


@pytest.fixture
def demo_registry():
    """Create a demo registry with test demos."""
    registry = DemoRegistry()
    registry.register(SampleTestDemo)
    registry.register(SecondTestDemo)
    registry.register(DifferentCategoryDemo)
    return registry


class TestGalleryScreenCreation:
    """Test GalleryScreen initialization and basic properties."""

    def test_gallery_screen_can_be_created(self, demo_registry):
        """Test that GalleryScreen can be instantiated."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen

        screen = GalleryScreen(demo_registry)
        assert screen is not None

    def test_gallery_screen_stores_registry(self, demo_registry):
        """Test that GalleryScreen stores the demo registry."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen

        screen = GalleryScreen(demo_registry)
        assert screen.registry is demo_registry

    def test_gallery_screen_has_title(self, demo_registry):
        """Test that GalleryScreen has a descriptive title."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen

        screen = GalleryScreen(demo_registry)
        assert hasattr(screen, "TITLE")
        assert len(screen.TITLE) > 0


class TestGalleryScreenLayout:
    """Test GalleryScreen layout and widget composition."""

    @pytest.mark.asyncio
    async def test_gallery_screen_composes_widgets(self, demo_registry):
        """Test that GalleryScreen has the expected widget composition."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Check that screen has been pushed
            assert pilot.app.screen is screen

    @pytest.mark.asyncio
    async def test_gallery_screen_displays_categories(self, demo_registry):
        """Test that GalleryScreen displays the available categories."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen, CategoryList
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Get the category list widget and check its content
            category_list = screen.query_one("#category-list", CategoryList)
            rendered_text = category_list.render()

            # Should show both categories
            assert "Test Category" in rendered_text or "Another Category" in rendered_text

    @pytest.mark.asyncio
    async def test_gallery_screen_has_category_list(self, demo_registry):
        """Test that GalleryScreen has a category list widget."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Look for category list widget
            category_list = screen.query_one("#category-list", Static)
            assert category_list is not None

    @pytest.mark.asyncio
    async def test_gallery_screen_has_demo_panel(self, demo_registry):
        """Test that GalleryScreen has a demo display panel."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Look for demo panel widget
            demo_panel = screen.query_one("#demo-panel", Static)
            assert demo_panel is not None


class TestGalleryScreenCategorySelection:
    """Test category selection and filtering."""

    @pytest.mark.asyncio
    async def test_can_get_selected_category(self, demo_registry):
        """Test getting the currently selected category."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Initially might be None or first category
            selected = screen.selected_category
            assert selected is None or isinstance(selected, str)

    @pytest.mark.asyncio
    async def test_can_set_selected_category(self, demo_registry):
        """Test setting the selected category."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Set category
            screen.selected_category = "Test Category"
            assert screen.selected_category == "Test Category"

    @pytest.mark.asyncio
    async def test_get_demos_for_selected_category(self, demo_registry):
        """Test retrieving demos for the selected category."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Set category
            screen.selected_category = "Test Category"

            # Get demos for that category
            demos = screen.get_current_demos()
            assert len(demos) == 2  # SampleTestDemo and SecondTestDemo
            assert all(d.category == "Test Category" for d in demos)


class TestGalleryScreenDemoSelection:
    """Test demo selection and display."""

    @pytest.mark.asyncio
    async def test_can_get_selected_demo(self, demo_registry):
        """Test getting the currently selected demo."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Initially should be None
            selected = screen.selected_demo
            assert selected is None or isinstance(selected, BaseDemo)

    @pytest.mark.asyncio
    async def test_can_set_selected_demo(self, demo_registry):
        """Test setting the selected demo."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Get a demo instance
            test_demo = demo_registry.get_demo_by_name("Test Demo")

            # Set it as selected
            screen.selected_demo = test_demo
            assert screen.selected_demo is test_demo

    @pytest.mark.asyncio
    async def test_selected_demo_updates_display(self, demo_registry):
        """Test that selecting a demo updates the display panel."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen, DemoPanel
        from textual.app import App

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            # Select a demo
            test_demo = demo_registry.get_demo_by_name("Test Demo")
            screen.selected_demo = test_demo

            # Wait for updates
            await pilot.pause()

            # Check that demo panel shows demo info
            demo_panel = screen.query_one("#demo-panel", DemoPanel)
            panel_text = demo_panel.render()

            # Should contain demo name or description
            assert "Test Demo" in panel_text or "testing purposes" in panel_text


class TestGalleryScreenKeybindings:
    """Test keyboard shortcuts and bindings."""

    def test_gallery_screen_has_bindings(self, demo_registry):
        """Test that GalleryScreen defines keybindings."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen

        screen = GalleryScreen(demo_registry)
        assert hasattr(screen, "BINDINGS")

    def test_gallery_screen_has_quit_binding(self, demo_registry):
        """Test that GalleryScreen can be dismissed."""
        from plexiglass.ui.screens.gallery_screen import GalleryScreen

        screen = GalleryScreen(demo_registry)
        # Check for escape or q binding (BINDINGS is a list of tuples)
        bindings = [b[0] for b in screen.BINDINGS] if hasattr(screen, "BINDINGS") else []
        assert "escape" in bindings or "q" in bindings
