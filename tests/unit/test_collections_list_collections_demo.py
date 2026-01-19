"""
Tests for ListCollectionsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.collections.list_collections import ListCollectionsDemo


class TestListCollectionsDemo:
    """Unit tests for ListCollectionsDemo."""

    def test_demo_metadata(self):
        demo = ListCollectionsDemo()

        assert demo.name == "List Collections"
        assert demo.category == "Collections & Playlists"
        assert demo.operation_type == "READ"

    def test_demo_parameters(self):
        demo = ListCollectionsDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "section_name"

    def test_demo_execute_with_none_server(self):
        demo = ListCollectionsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_collections(self):
        demo = ListCollectionsDemo()

        collection = MagicMock()
        collection.title = "Favorites"
        collection.ratingKey = "col-1"

        section = MagicMock()
        section.collections.return_value = [collection]

        server = MagicMock()
        server.library.section.return_value = section

        result = demo.execute(server=server, params={"section_name": "Movies"})

        assert "collections" in result
        assert result["collections"][0]["title"] == "Favorites"
