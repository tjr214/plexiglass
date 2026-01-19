"""
Tests for ListLibraryItemsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.library.list_library_items import ListLibraryItemsDemo


class TestListLibraryItemsDemo:
    """Unit tests for ListLibraryItemsDemo."""

    def test_demo_metadata(self):
        demo = ListLibraryItemsDemo()

        assert demo.name == "List Library Items"
        assert demo.category == "Library Management"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = ListLibraryItemsDemo()
        code = demo.get_code_example()

        assert "section" in code

    def test_demo_parameters(self):
        demo = ListLibraryItemsDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "section_name"

    def test_demo_execute_with_none_server(self):
        demo = ListLibraryItemsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_items(self):
        demo = ListLibraryItemsDemo()

        item = MagicMock()
        item.title = "Item"
        item.type = "movie"
        item.ratingKey = "123"

        section = MagicMock()
        section.all.return_value = [item]

        server = MagicMock()
        server.library.section.return_value = section

        result = demo.execute(server=server, params={"section_name": "Movies"})

        assert "items" in result
        assert result["items"][0]["title"] == "Item"
