"""
Tests for ListSharedLibrariesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.users.list_shared_libraries import ListSharedLibrariesDemo


class TestListSharedLibrariesDemo:
    """Unit tests for ListSharedLibrariesDemo."""

    def test_demo_metadata(self):
        demo = ListSharedLibrariesDemo()

        assert demo.name == "List Shared Libraries"
        assert demo.category == "Users & Sharing"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListSharedLibrariesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_shares(self):
        demo = ListSharedLibrariesDemo()

        share = MagicMock()
        share.title = "Family Library"
        share.sections = ["Movies", "Shows"]

        account = MagicMock()
        account.sharedLibraries.return_value = [share]

        server = MagicMock()
        server.myPlexAccount.return_value = account

        result = demo.execute(server=server, params={})

        assert "shared_libraries" in result
        assert result["shared_libraries"][0]["title"] == "Family Library"
