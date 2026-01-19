"""
Tests for RecentPlaysDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.playback.list_recent_plays import ListRecentPlaysDemo


class TestListRecentPlaysDemo:
    """Unit tests for ListRecentPlaysDemo."""

    def test_demo_metadata(self):
        demo = ListRecentPlaysDemo()

        assert demo.name == "List Recent Plays"
        assert demo.category == "Playback & Clients"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListRecentPlaysDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_plays(self):
        demo = ListRecentPlaysDemo()

        entry = MagicMock()
        entry.title = "Movie"
        entry.type = "movie"
        entry.viewedAt = 123456

        server = MagicMock()
        server.history.return_value = [entry]

        result = demo.execute(server=server, params={})

        assert "recent_plays" in result
        assert result["recent_plays"][0]["title"] == "Movie"
        assert result["recent_plays"][0]["type"] == "movie"
