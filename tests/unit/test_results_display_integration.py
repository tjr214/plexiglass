"""
Integration tests for ResultsDisplay widget in a Textual app context.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.scrollable_results import ScrollableResults


class TestResultsDisplayIntegration:
    """Integration tests for ResultsDisplay rendering."""

    @pytest.mark.asyncio
    async def test_results_display_can_mount(self):
        """ResultsDisplay can mount inside a Textual app."""

        class TestApp(App):
            def compose(self):
                yield ScrollableResults(id="results-display")

        app = TestApp()
        async with app.run_test() as pilot:
            display = pilot.app.query_one("#results-display", ScrollableResults)
            assert display is not None
