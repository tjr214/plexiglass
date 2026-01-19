"""
Tests for ListServerLibrariesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.server.list_server_libraries import ListServerLibrariesDemo


class TestListServerLibrariesDemo:
    """Unit tests for ListServerLibrariesDemo."""

    def test_demo_metadata(self):
        demo = ListServerLibrariesDemo()

        assert demo.name == "List Server Libraries"
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = ListServerLibrariesDemo()
        code = demo.get_code_example()

        assert "library" in code

    def test_demo_execute_with_none_server(self):
        demo = ListServerLibrariesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_sections(self):
        demo = ListServerLibrariesDemo()

        section = MagicMock()
        section.title = "Movies"
        section.type = "movie"
        section.uuid = "uuid-123"

        server = MagicMock()
        server.library.sections.return_value = [section]

        result = demo.execute(server=server, params={})

        assert "libraries" in result
        assert result["libraries"][0]["title"] == "Movies"
        assert result["libraries"][0]["type"] == "movie"
