"""
Tests for ListServerSessionsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.server.list_server_sessions import ListServerSessionsDemo


class TestListServerSessionsDemo:
    """Unit tests for ListServerSessionsDemo."""

    def test_demo_metadata(self):
        demo = ListServerSessionsDemo()

        assert demo.name == "List Server Sessions"
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = ListServerSessionsDemo()
        code = demo.get_code_example()

        assert "sessions" in code

    def test_demo_execute_with_none_server(self):
        demo = ListServerSessionsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_sessions(self):
        demo = ListServerSessionsDemo()
        session = MagicMock()
        session.title = "Movie"
        session.usernames = ["viewer"]
        session.state = "playing"
        session.viewOffset = 10
        session.duration = 100

        server = MagicMock()
        server.sessions.return_value = [session]

        result = demo.execute(server=server, params={})

        assert "sessions" in result
        assert result["sessions"][0]["title"] == "Movie"
        assert result["sessions"][0]["user"] == "viewer"
