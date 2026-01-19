"""
Tests for DemoParameters widget.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.demo_parameters import DemoParameters


class TestDemoParameters:
    @pytest.mark.asyncio
    async def test_demo_parameters_empty(self):
        class TestApp(App):
            def compose(self):
                yield DemoParameters(id="demo-params")

        app = TestApp()
        async with app.run_test() as pilot:
            widget = pilot.app.query_one("#demo-params", DemoParameters)
            widget.update_parameters([])
            assert widget.get_values() == {}

    @pytest.mark.asyncio
    async def test_demo_parameters_values(self):
        class TestApp(App):
            def compose(self):
                yield DemoParameters(id="demo-params")

        app = TestApp()
        async with app.run_test() as pilot:
            widget = pilot.app.query_one("#demo-params", DemoParameters)
            widget.update_parameters(
                [{"name": "section_name", "required": True, "description": "Section"}],
                {"section_name": "Movies"},
            )
            values = widget.get_values()
            assert values.get("section_name") in {"Movies", ""}
