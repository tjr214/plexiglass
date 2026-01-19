"""
Tests for ResultsDisplay widget.

The ResultsDisplay shows formatted demo execution output.
"""

from __future__ import annotations

from plexiglass.ui.widgets.results_display import ResultsDisplay


class TestResultsDisplay:
    """Unit tests for ResultsDisplay widget."""

    def test_results_display_initial_state(self):
        """ResultsDisplay shows placeholder when no results set."""
        display = ResultsDisplay()

        assert display.results is None
        assert display.render() == "Run a demo to see results"

    def test_results_display_set_results_updates_render(self):
        """Setting results renders a formatted string."""
        display = ResultsDisplay()
        results = {"status": "success", "items": ["a", "b"]}

        display.set_results(results)
        rendered = display.render()

        assert display.results == results
        assert isinstance(rendered, str)
        assert "status" in rendered
        assert "success" in rendered

    def test_results_display_clear_results_resets_placeholder(self):
        """Clearing results resets placeholder text."""
        display = ResultsDisplay()
        display.set_results({"status": "ok"})
        display.set_results(None)

        assert display.results is None
        assert display.render() == "Run a demo to see results"
