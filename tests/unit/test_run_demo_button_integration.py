"""
Integration tests for RunDemoButton widget.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.run_demo_button import RunDemoButton


class TestRunDemoButtonIntegration:
    @pytest.mark.asyncio
    async def test_run_demo_button_can_mount(self):
        class TestApp(App):
            def compose(self):
                yield RunDemoButton(id="run-demo")

        app = TestApp()
        async with app.run_test() as pilot:
            button = pilot.app.query_one("#run-demo", RunDemoButton)
            assert button is not None
