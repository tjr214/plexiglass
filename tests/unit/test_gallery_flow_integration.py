"""
End-to-end integration tests for GalleryScreen flow.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


class FlowDemo(BaseDemo):
    """Demo used for gallery flow integration tests."""

    name = "Flow Demo"
    description = "Demo for flow test"
    category = "Server & Connection"
    operation_type = "READ"

    def execute(self, server, params):
        return {"status": "ok"}

    def get_code_example(self, params=None):
        return "server.sessions()"


@pytest.fixture
def demo_registry():
    registry = DemoRegistry()
    registry.register(FlowDemo)
    return registry


class TestGalleryFlowIntegration:
    """Integration tests for gallery flow interactions."""

    @pytest.mark.asyncio
    async def test_gallery_flow_updates_demo_and_code_viewer(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import DemoPanel, GalleryScreen
        from plexiglass.ui.widgets.code_viewer import CodeViewer
        from plexiglass.ui.widgets.results_display import ResultsDisplay

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            demo = demo_registry.get_demo_by_name("Flow Demo")
            screen.selected_demo = demo
            await pilot.pause()

            demo_panel = screen.query_one("#demo-summary", DemoPanel)
            code_viewer = screen.query_one("#code-viewer", CodeViewer)
            results_display = screen.query_one("#results-display", ResultsDisplay)

            assert "Flow Demo" in demo_panel.render()
            assert code_viewer.code == "server.sessions()"
            assert results_display.render() == "Run a demo to see results"

    @pytest.mark.asyncio
    async def test_gallery_flow_clears_demo_state(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import DemoPanel, GalleryScreen
        from plexiglass.ui.widgets.code_viewer import CodeViewer

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            demo = demo_registry.get_demo_by_name("Flow Demo")
            screen.selected_demo = demo
            await pilot.pause()

            screen.selected_demo = None
            await pilot.pause()

            demo_panel = screen.query_one("#demo-summary", DemoPanel)
            code_viewer = screen.query_one("#code-viewer", CodeViewer)

            assert demo_panel.render() == "Select a category and demo to view details"
            assert code_viewer.code is None
