"""
Tests for UndoButton widget.
"""

from __future__ import annotations

from textual.widgets import Button

from plexiglass.ui.widgets.undo_button import UndoButton


class TestUndoButton:
    """Unit tests for UndoButton widget."""

    def test_undo_button_initial_state(self):
        button = UndoButton()

        assert button.can_undo is False
        assert button.disabled is True
        assert str(button.label) == "Undo"

    def test_undo_button_updates_state(self):
        button = UndoButton()

        button.set_can_undo(True)
        assert button.can_undo is True
        assert button.disabled is False

        button.set_can_undo(False)
        assert button.can_undo is False
        assert button.disabled is True

    def test_undo_button_is_button(self):
        button = UndoButton()
        assert isinstance(button, Button)
