"""
Integration tests for ResultsDisplay widget in a Textual app context.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.results_display import ResultsDisplay


class TestResultsDisplayIntegration:
    """Integration tests for ResultsDisplay rendering."""

    @pytest.mark.asyncio
    async def test_results_display_can_mount(self):
        """ResultsDisplay can mount inside a Textual app."""

        class TestApp(App):
            def compose(self):
                yield ResultsDisplay(id="results-display")

        app = TestApp()
        async with app.run_test() as pilot:
            display = pilot.app.query_one("#results-display", ResultsDisplay)
            assert display is not None
