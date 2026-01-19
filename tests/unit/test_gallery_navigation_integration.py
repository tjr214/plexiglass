"""
Integration tests for gallery navigation flow.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


class NavDemo(BaseDemo):
    name = "Nav Demo"
    description = "Navigation demo"
    category = "Server & Connection"
    operation_type = "READ"

    def execute(self, server, params):
        return {"ok": True}


@pytest.fixture
def demo_registry():
    registry = DemoRegistry()
    registry.register(NavDemo)
    return registry


class TestGalleryNavigationIntegration:
    @pytest.mark.asyncio
    async def test_gallery_category_selection_updates_demo_list(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.demo_list import DemoList

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            screen.selected_category = "Server & Connection"
            await pilot.pause()

            demo_list = screen.query_one("#demo-list", DemoList)
            assert demo_list._demo_map
            assert demo_list._demo_map[0].name == "Nav Demo"
