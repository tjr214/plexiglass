"""
Tests for ListShowsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.media.list_shows import ListShowsDemo


class TestListShowsDemo:
    """Unit tests for ListShowsDemo."""

    def test_demo_metadata(self):
        demo = ListShowsDemo()

        assert demo.name == "List Shows"
        assert demo.category == "Media Operations"
        assert demo.operation_type == "READ"

    def test_demo_parameters(self):
        demo = ListShowsDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "section_name"

    def test_demo_execute_with_none_server(self):
        demo = ListShowsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_shows(self):
        demo = ListShowsDemo()

        item = MagicMock()
        item.title = "Show"
        item.type = "show"
        item.ratingKey = "789"

        section = MagicMock()
        section.all.return_value = [item]

        server = MagicMock()
        server.library.section.return_value = section

        result = demo.execute(server=server, params={"section_name": "Shows"})

        assert "shows" in result
        assert result["shows"][0]["title"] == "Show"
