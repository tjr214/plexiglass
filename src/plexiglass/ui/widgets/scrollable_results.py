"""
ScrollableResults widget for PlexiGlass Gallery.

Wraps ResultsDisplay in a VerticalScroll container.
"""

from __future__ import annotations

from textual.containers import VerticalScroll
from textual.widgets import RichLog


class ScrollableResults(VerticalScroll):
    """Scrollable container for results display."""

    DEFAULT_CSS = """
    ScrollableResults {
        border: round $primary;
        background: $surface;
        padding: 1;
        height: 1fr;
        overflow-y: auto;
        scrollbar-gutter: stable;
        scrollbar-visibility: visible;
    }

    ScrollableResults > RichLog {
        width: 100%;
        height: auto;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._log = RichLog(highlight=False)
        self._last_render = "Run a demo to see results"

    def on_mount(self) -> None:
        self.mount(self._log)
        self._log.write(self._last_render)

    def set_results(self, results: object | None) -> None:
        """Render results into the scrollable log."""
        self._log.clear()
        if results is None:
            self._last_render = "Run a demo to see results"
            self._log.write(self._last_render)
            return
        self._last_render = str(results)
        self._log.write(results)

    def get_rendered(self) -> str:
        return self._last_render
