"""
Integration tests for UndoButton within GalleryScreen.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.registry import DemoRegistry


@pytest.fixture
def demo_registry():
    return DemoRegistry()


class TestGalleryScreenUndoButtonIntegration:
    """Validate GalleryScreen wires an UndoButton."""

    @pytest.mark.asyncio
    async def test_gallery_screen_has_undo_button(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.undo_button import UndoButton

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            undo_button = screen.query_one("#undo-button", UndoButton)
            assert undo_button is not None
