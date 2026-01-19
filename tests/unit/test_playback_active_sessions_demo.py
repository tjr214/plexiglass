"""
Tests for ListPlaybackSessionsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.playback.list_playback_sessions import ListPlaybackSessionsDemo


class TestListPlaybackSessionsDemo:
    """Unit tests for ListPlaybackSessionsDemo."""

    def test_demo_metadata(self):
        demo = ListPlaybackSessionsDemo()

        assert demo.name == "List Playback Sessions"
        assert demo.category == "Playback & Clients"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListPlaybackSessionsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_sessions(self):
        demo = ListPlaybackSessionsDemo()

        player = MagicMock()
        player.title = "Living Room"
        session = MagicMock()
        session.title = "Episode"
        session.players = [player]
        session.state = "playing"

        server = MagicMock()
        server.sessions.return_value = [session]

        result = demo.execute(server=server, params={})

        assert "sessions" in result
        assert result["sessions"][0]["title"] == "Episode"
        assert result["sessions"][0]["player"] == "Living Room"
