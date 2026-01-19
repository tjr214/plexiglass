"""
Tests for ResultsDisplay widget.

The ResultsDisplay shows formatted demo execution output.
"""

from __future__ import annotations

from plexiglass.ui.widgets.scrollable_results import ScrollableResults


class TestResultsDisplay:
    """Unit tests for ResultsDisplay widget."""

    def test_results_display_initial_state(self):
        """ResultsDisplay shows placeholder when no results set."""
        display = ScrollableResults()

        assert display.get_rendered() == "Run a demo to see results"

    def test_results_display_set_results_updates_render(self):
        """Setting results renders a formatted string."""
        display = ScrollableResults()
        results = {"status": "success", "items": ["a", "b"]}

        display.set_results(results)
        rendered = display.get_rendered()

        assert isinstance(rendered, str)
        assert "status" in rendered
        assert "success" in rendered

    def test_results_display_clear_results_resets_placeholder(self):
        """Clearing results resets placeholder text."""
        display = ScrollableResults()
        display.set_results({"status": "ok"})
        display.set_results(None)

        assert display.get_rendered() == "Run a demo to see results"
