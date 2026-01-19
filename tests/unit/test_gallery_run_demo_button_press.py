"""
Tests for run demo button press handler.
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


class TestGalleryRunDemoButtonPress:
    @pytest.mark.asyncio
    async def test_run_demo_button_press_runs_demo(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.scrollable_results import ScrollableResults
        from plexiglass.ui.widgets.run_demo_button import RunDemoButton

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

            run_button = screen.query_one("#run-demo", RunDemoButton)
            run_button.press()
            await pilot.pause()

            results_display = screen.query_one("#results-display", ScrollableResults)
            rendered = results_display.get_rendered()
            assert "status" in rendered
