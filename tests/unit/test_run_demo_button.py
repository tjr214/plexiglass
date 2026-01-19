"""
Tests for RunDemoButton widget.
"""

from __future__ import annotations

from textual.widgets import Button

from plexiglass.ui.widgets.run_demo_button import RunDemoButton


class TestRunDemoButton:
    def test_button_initial_state(self):
        button = RunDemoButton()

        assert button.disabled is True
        assert isinstance(button, Button)

    def test_button_enable_toggle(self):
        button = RunDemoButton()

        button.set_enabled(True)
        assert button.disabled is False

        button.set_enabled(False)
        assert button.disabled is True
