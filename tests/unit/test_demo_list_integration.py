"""
Integration tests for DemoList widget.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.ui.widgets.demo_list import DemoList


class SampleDemo(BaseDemo):
    name = "Sample Demo"
    description = "Sample"
    category = "Samples"
    operation_type = "READ"

    def execute(self, server, params):
        return {"status": "ok"}


class TestDemoListIntegration:
    """Integration tests for DemoList rendering."""

    @pytest.mark.asyncio
    async def test_demo_list_can_mount(self):
        class TestApp(App):
            def compose(self):
                yield DemoList([SampleDemo()], id="demo-list")

        app = TestApp()
        async with app.run_test() as pilot:
            demo_list = pilot.app.query_one("#demo-list", DemoList)
            assert demo_list is not None
