"""
Integration tests for CodeViewer widget with Textual app context.
"""

from __future__ import annotations

import pytest
from textual.app import App

from plexiglass.ui.widgets.code_viewer import CodeViewer


class TestCodeViewerIntegration:
    """Integration tests for CodeViewer rendering in a Textual app."""

    @pytest.mark.asyncio
    async def test_code_viewer_can_mount(self):
        """CodeViewer can mount inside a Textual app."""

        class TestApp(App):
            def compose(self):
                yield CodeViewer(id="code-viewer")

        app = TestApp()
        async with app.run_test() as pilot:
            viewer = pilot.app.query_one("#code-viewer", CodeViewer)
            assert viewer is not None
