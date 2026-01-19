"""
Tests for SearchLibraryDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.library.search_library import SearchLibraryDemo


class TestSearchLibraryDemo:
    """Unit tests for SearchLibraryDemo."""

    def test_demo_metadata(self):
        demo = SearchLibraryDemo()

        assert demo.name == "Search Library"
        assert demo.category == "Library Management"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = SearchLibraryDemo()
        code = demo.get_code_example()

        assert "search" in code

    def test_demo_parameters(self):
        demo = SearchLibraryDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "query"

    def test_demo_execute_with_none_server(self):
        demo = SearchLibraryDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_results(self):
        demo = SearchLibraryDemo()

        item = MagicMock()
        item.title = "Alien"
        item.type = "movie"
        item.ratingKey = "456"

        server = MagicMock()
        server.library.search.return_value = [item]

        result = demo.execute(server=server, params={"query": "Alien"})

        assert "results" in result
        assert result["results"][0]["title"] == "Alien"
