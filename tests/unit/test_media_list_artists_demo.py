"""
Tests for ListArtistsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.media.list_artists import ListArtistsDemo


class TestListArtistsDemo:
    """Unit tests for ListArtistsDemo."""

    def test_demo_metadata(self):
        demo = ListArtistsDemo()

        assert demo.name == "List Artists"
        assert demo.category == "Media Operations"
        assert demo.operation_type == "READ"

    def test_demo_parameters(self):
        demo = ListArtistsDemo()
        params = demo.get_parameters()

        assert params
        assert params[0]["name"] == "section_name"

    def test_demo_execute_with_none_server(self):
        demo = ListArtistsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_artists(self):
        demo = ListArtistsDemo()

        item = MagicMock()
        item.title = "Artist"
        item.type = "artist"
        item.ratingKey = "456"

        section = MagicMock()
        section.all.return_value = [item]

        server = MagicMock()
        server.library.section.return_value = section

        result = demo.execute(server=server, params={"section_name": "Music"})

        assert "artists" in result
        assert result["artists"][0]["title"] == "Artist"
