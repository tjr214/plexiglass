"""
UndoButton widget for PlexiGlass.
"""

from __future__ import annotations

from textual.widgets import Button


class UndoButton(Button):
    """Button for triggering undo operations."""

    DEFAULT_CSS = """
    UndoButton {
        background: $warning;
        color: $text;
        border: round $warning-darken-2;
        padding: 0 2;
    }

    UndoButton:disabled {
        background: $surface;
        color: $text-muted;
        border: round $surface-lighten-1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("Undo", **kwargs)
        self.can_undo = False
        self.disabled = True

    def set_can_undo(self, can_undo: bool) -> None:
        """Update enabled state based on undo availability."""
        self.can_undo = can_undo
        self.disabled = not can_undo
