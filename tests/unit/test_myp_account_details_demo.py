"""
Tests for MyPlexAccountDetailsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.myp.account_details import MyPlexAccountDetailsDemo


class TestMyPlexAccountDetailsDemo:
    """Unit tests for MyPlexAccountDetailsDemo."""

    def test_demo_metadata(self):
        demo = MyPlexAccountDetailsDemo()

        assert demo.name == "MyPlex Account Details"
        assert demo.category == "MyPlex Account"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = MyPlexAccountDetailsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_account_info(self):
        demo = MyPlexAccountDetailsDemo()

        account = MagicMock()
        account.title = "Admin"
        account.username = "admin"
        account.email = "admin@example.com"
        account.id = 101

        server = MagicMock()
        server.myPlexAccount.return_value = account

        result = demo.execute(server=server, params={})

        assert "account" in result
        assert result["account"]["title"] == "Admin"
