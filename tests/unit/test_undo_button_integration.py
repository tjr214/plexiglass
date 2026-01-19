"""
Integration tests for UndoButton widget.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.undo_button import UndoButton


class TestUndoButtonIntegration:
    """Integration tests for UndoButton rendering."""

    @pytest.mark.asyncio
    async def test_undo_button_can_mount(self):
        class TestApp(App):
            def compose(self):
                yield UndoButton(id="undo-button")

        app = TestApp()
        async with app.run_test() as pilot:
            button = pilot.app.query_one("#undo-button", UndoButton)
            assert button is not None
