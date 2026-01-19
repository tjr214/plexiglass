"""
Tests for ListPlaylistsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.collections.list_playlists import ListPlaylistsDemo


class TestListPlaylistsDemo:
    """Unit tests for ListPlaylistsDemo."""

    def test_demo_metadata(self):
        demo = ListPlaylistsDemo()

        assert demo.name == "List Playlists"
        assert demo.category == "Collections & Playlists"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListPlaylistsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_playlists(self):
        demo = ListPlaylistsDemo()

        playlist = MagicMock()
        playlist.title = "Road Trip"
        playlist.playlistType = "audio"
        playlist.ratingKey = "pl-1"

        server = MagicMock()
        server.playlists.return_value = [playlist]

        result = demo.execute(server=server, params={})

        assert "playlists" in result
        assert result["playlists"][0]["title"] == "Road Trip"
