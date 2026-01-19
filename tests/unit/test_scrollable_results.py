"""
Tests for ScrollableResults widget.
"""

from __future__ import annotations

from plexiglass.ui.widgets.scrollable_results import ScrollableResults


class TestScrollableResults:
    def test_scrollable_results_proxy(self):
        widget = ScrollableResults()
        widget.set_results({"status": "ok"})
        rendered = widget.get_rendered()
        assert "status" in rendered
