"""
ResultsDisplay widget for PlexiGlass Gallery.

Displays formatted demo execution output.
"""

from __future__ import annotations

import json
from pprint import pformat

from textual.widgets import Static


class ResultsDisplay(Static):
    """Widget for displaying demo results."""

    DEFAULT_CSS = """
    ResultsDisplay {
        border: round $primary;
        background: $surface;
        padding: 1 2;
        height: 1fr;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.results: object | None = None
        self.add_class("results-display")

    def set_results(self, results: object | None) -> None:
        """Set the results to display."""
        self.results = results
        self.update(self.render())

    def _format_results(self, results: object) -> str:
        """Format results for display."""
        try:
            return json.dumps(results, indent=2, sort_keys=True, default=str)
        except (TypeError, ValueError):
            return pformat(results)

    def render(self):
        """Render the results display."""
        if self.results is None:
            return "Run a demo to see results"
        return self._format_results(self.results)
