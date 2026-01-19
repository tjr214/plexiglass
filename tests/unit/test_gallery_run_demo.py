"""
Tests for running demos from GalleryScreen.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from textual.app import App

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.gallery.registry import DemoRegistry


class RunDemo(BaseDemo):
    name = "Run Demo"
    description = "Run demo"
    category = "Server & Connection"
    operation_type = "READ"

    def execute(self, server, params):
        return {"status": "ok"}


@pytest.fixture
def demo_registry():
    registry = DemoRegistry()
    registry.register(RunDemo)
    return registry


class TestGalleryRunDemo:
    @pytest.mark.asyncio
    async def test_run_demo_updates_results(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.results_display import ResultsDisplay

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        setattr(app, "server_manager", MagicMock())
        app_server_manager = getattr(app, "server_manager")
        app_server_manager.connect_to_default.return_value = MagicMock()

        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)
            screen.selected_demo = demo_registry.get_demo_by_name("Run Demo")
            screen.action_run_demo()

            results_display = screen.query_one("#results-display", ResultsDisplay)
            assert results_display.render() == "{'status': 'ok'}" or "status" in str(
                results_display.render()
            )
