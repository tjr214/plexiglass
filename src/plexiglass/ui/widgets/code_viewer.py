"""
CodeViewer widget for PlexiGlass Gallery.

Displays code examples with syntax highlighting.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.syntax import Syntax
from textual.widgets import Static

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo


class CodeViewer(Static):
    """Widget for displaying demo code examples."""

    DEFAULT_CSS = """
    CodeViewer {
        border: round $primary;
        background: $surface;
        padding: 1 2;
        height: 1fr;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.code: str | None = None
        self.add_class("code-viewer")

    def set_code(self, code: str | None) -> None:
        """Set the code snippet to display."""
        self.code = code
        self.update(self.render())

    def set_demo(self, demo: BaseDemo | None) -> None:
        """Set the demo and display its code example."""
        if demo is None:
            self.set_code(None)
            return
        self.set_code(demo.get_code_example())

    def render(self):
        """Render the code snippet with syntax highlighting."""
        if not self.code:
            return "Select a demo to view code"
        return Syntax(self.code, "python", line_numbers=True)
