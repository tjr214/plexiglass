"""
RunDemoButton widget for PlexiGlass.
"""

from __future__ import annotations

from textual.widgets import Button


class RunDemoButton(Button):
    """Button for running a selected demo."""

    DEFAULT_CSS = """
    RunDemoButton {
        background: $success;
        color: $text;
        border: round $success-darken-2;
        padding: 0 2;
    }

    RunDemoButton:disabled {
        background: $surface;
        color: $text-muted;
        border: round $surface-lighten-1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("Run Demo", **kwargs)
        self.disabled = True

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable the button."""
        self.disabled = not enabled
