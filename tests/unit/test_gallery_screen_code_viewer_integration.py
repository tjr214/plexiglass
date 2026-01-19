"""
Integration tests for CodeViewer within GalleryScreen.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


class SampleCodeDemo(BaseDemo):
    """Sample demo providing a code example."""

    name = "Sample Code Demo"
    description = "Demo with code example"
    category = "Server & Connection"
    operation_type = "READ"

    def execute(self, server, params):
        return {"result": "ok"}

    def get_code_example(self, params=None):
        return "server.library.sections()"


@pytest.fixture
def demo_registry():
    registry = DemoRegistry()
    registry.register(SampleCodeDemo)
    return registry


class TestGalleryScreenCodeViewerIntegration:
    """Validate GalleryScreen wires a CodeViewer."""

    @pytest.mark.asyncio
    async def test_gallery_screen_has_code_viewer(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.code_viewer import CodeViewer

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            code_viewer = screen.query_one("#code-viewer", CodeViewer)
            assert code_viewer is not None
