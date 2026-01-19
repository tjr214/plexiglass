"""
Tests for ListUsersDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.users.list_users import ListUsersDemo


class TestListUsersDemo:
    """Unit tests for ListUsersDemo."""

    def test_demo_metadata(self):
        demo = ListUsersDemo()

        assert demo.name == "List Users"
        assert demo.category == "Users & Sharing"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListUsersDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_users(self):
        demo = ListUsersDemo()

        user = MagicMock()
        user.title = "Viewer"
        user.email = "viewer@example.com"
        user.id = 42

        account = MagicMock()
        account.users.return_value = [user]

        server = MagicMock()
        server.myPlexAccount.return_value = account

        result = demo.execute(server=server, params={})

        assert "users" in result
        assert result["users"][0]["title"] == "Viewer"
