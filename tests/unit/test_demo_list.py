"""
Tests for DemoList widget.
"""

from __future__ import annotations

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

        assert demo_list._demo_map[0].name == "Sample Demo"
