"""
Integration tests for ResultsDisplay within GalleryScreen.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.registry import DemoRegistry


@pytest.fixture
def demo_registry():
    return DemoRegistry()


class TestGalleryScreenResultsDisplayIntegration:
    """Validate GalleryScreen wires a ResultsDisplay."""

    @pytest.mark.asyncio
    async def test_gallery_screen_has_results_display(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.scrollable_results import ScrollableResults

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            results_display = screen.query_one("#results-display", ScrollableResults)
            assert results_display is not None
