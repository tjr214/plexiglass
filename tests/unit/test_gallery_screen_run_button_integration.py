"""
Integration tests for RunDemoButton within GalleryScreen.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.registry import DemoRegistry


@pytest.fixture
def demo_registry():
    return DemoRegistry()


class TestGalleryScreenRunButtonIntegration:
    """Validate GalleryScreen wires a RunDemoButton."""

    @pytest.mark.asyncio
    async def test_gallery_screen_has_run_button(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.run_demo_button import RunDemoButton

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            run_button = screen.query_one("#run-demo", RunDemoButton)
            assert run_button is not None
