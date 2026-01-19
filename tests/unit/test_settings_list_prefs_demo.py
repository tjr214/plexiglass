"""
Tests for ListServerPreferencesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.settings.list_server_preferences import ListServerPreferencesDemo


class TestListServerPreferencesDemo:
    """Unit tests for ListServerPreferencesDemo."""

    def test_demo_metadata(self):
        demo = ListServerPreferencesDemo()

        assert demo.name == "List Server Preferences"
        assert demo.category == "Settings"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListServerPreferencesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_prefs(self):
        demo = ListServerPreferencesDemo()

        pref = MagicMock()
        pref.id = "pref.id"
        pref.value = "true"
        pref.summary = "Preference summary"

        server = MagicMock()
        server.preferences.return_value = [pref]

        result = demo.execute(server=server, params={})

        assert "preferences" in result
        assert result["preferences"][0]["id"] == "pref.id"
