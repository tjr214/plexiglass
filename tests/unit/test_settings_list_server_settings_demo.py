"""
Tests for ListServerSettingsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.settings.list_server_settings import ListServerSettingsDemo


class TestListServerSettingsDemo:
    """Unit tests for ListServerSettingsDemo."""

    def test_demo_metadata(self):
        demo = ListServerSettingsDemo()

        assert demo.name == "List Server Settings"
        assert demo.category == "Settings"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = ListServerSettingsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_settings(self):
        demo = ListServerSettingsDemo()

        setting = MagicMock()
        setting.id = "settings.enabled"
        setting.value = "1"
        setting.summary = "Enable feature"

        server = MagicMock()
        server.settings.return_value = [setting]

        result = demo.execute(server=server, params={})

        assert "settings" in result
        assert result["settings"][0]["id"] == "settings.enabled"
