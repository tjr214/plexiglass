"""
Tests for DemoList widget.
"""

from __future__ import annotations

import pytest

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.ui.widgets.demo_list import DemoList


class SampleDemo(BaseDemo):
    name = "Sample Demo"
    description = "Sample"
    category = "Samples"
    operation_type = "READ"

    def execute(self, server, params):
        return {"status": "ok"}


class TestDemoList:
    """Unit tests for DemoList widget."""

    def test_demo_list_initial_state(self):
        demo_list = DemoList([])
        assert demo_list is not None

    def test_demo_list_updates_demos(self):
        demo_list = DemoList([])
        demo_list.update_demos([SampleDemo()])

        assert demo_list._demo_map == {}

    @pytest.mark.asyncio
    async def test_demo_list_updates_demos_when_mounted(self):
        from textual.app import App

        class TestApp(App):
            def compose(self):
                yield DemoList([], id="demo-list")

        app = TestApp()
        async with app.run_test() as pilot:
            demo_list = pilot.app.query_one("#demo-list", DemoList)
            demo_list.update_demos([SampleDemo()])
            assert demo_list._demo_map[0].name == "Sample Demo"
