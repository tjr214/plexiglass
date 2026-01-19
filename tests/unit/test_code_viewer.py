"""
Tests for CodeViewer widget.

The CodeViewer displays python-plexapi code snippets with syntax highlighting.
"""

from __future__ import annotations

from rich.syntax import Syntax

from plexiglass.gallery.base_demo import BaseDemo
from plexiglass.ui.widgets.code_viewer import CodeViewer


class SampleCodeDemo(BaseDemo):
    """Sample demo providing a code example."""

    name = "Sample Code Demo"
    description = "Demo with code example"
    category = "Server & Connection"
    operation_type = "READ"

    def execute(self, server, params):
        return {"result": "ok"}

    def get_code_example(self, params=None):
        return "server.sessions()"


class TestCodeViewer:
    """Test suite for CodeViewer widget."""

    def test_code_viewer_initial_state(self):
        """CodeViewer shows placeholder when no code is set."""
        viewer = CodeViewer()

        assert viewer.code is None
        assert viewer.render() == "Select a demo to view code"

    def test_code_viewer_set_code_updates_render(self):
        """Setting code updates the rendered syntax output."""
        viewer = CodeViewer()
        code = "print('hello')"

        viewer.set_code(code)
        rendered = viewer.render()

        assert viewer.code == code
        assert isinstance(rendered, Syntax)
        assert rendered.code == code

    def test_code_viewer_set_demo_uses_demo_code(self):
        """Setting a demo pulls code from the demo instance."""
        viewer = CodeViewer()
        demo = SampleCodeDemo()

        viewer.set_demo(demo)

        assert viewer.code == demo.get_code_example()
        assert isinstance(viewer.render(), Syntax)

    def test_code_viewer_clear_demo_resets_placeholder(self):
        """Clearing the demo resets the placeholder text."""
        viewer = CodeViewer()
        demo = SampleCodeDemo()

        viewer.set_demo(demo)
        viewer.set_demo(None)

        assert viewer.code is None
        assert viewer.render() == "Select a demo to view code"
