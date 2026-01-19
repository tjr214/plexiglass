"""
Integration tests for GalleryScreen undo flow.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.registry import DemoRegistry


@pytest.fixture
def demo_registry():
    return DemoRegistry()


class TestGalleryScreenUndoFlow:
    """Validate undo snapshot flow wiring in GalleryScreen."""

    @pytest.mark.asyncio
    async def test_undo_snapshot_enables_button_and_updates_results(self, demo_registry):
        from plexiglass.ui.screens.gallery_screen import GalleryScreen
        from plexiglass.ui.widgets.scrollable_results import ScrollableResults
        from plexiglass.ui.widgets.undo_button import UndoButton

        class TestApp(App):
            def on_mount(self):
                pass

        app = TestApp()
        async with app.run_test() as pilot:
            screen = GalleryScreen(demo_registry)
            await pilot.app.push_screen(screen)

            screen.record_undo_snapshot("update", {"item_id": 10})
            await pilot.pause()

            undo_button = screen.query_one("#undo-button", UndoButton)
            assert undo_button.disabled is False

            screen.perform_undo()
            await pilot.pause()

            results_display = screen.query_one("#results-display", ScrollableResults)
            rendered = results_display.get_rendered()
            assert "undo_operation" in rendered
            assert "update" in rendered
