"""
Tests for MyPlexDevicesDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.myp.list_devices import MyPlexDevicesDemo


class TestMyPlexDevicesDemo:
    """Unit tests for MyPlexDevicesDemo."""

    def test_demo_metadata(self):
        demo = MyPlexDevicesDemo()

        assert demo.name == "MyPlex Devices"
        assert demo.category == "MyPlex Account"
        assert demo.operation_type == "READ"

    def test_demo_execute_with_none_server(self):
        demo = MyPlexDevicesDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_devices(self):
        demo = MyPlexDevicesDemo()

        device = MagicMock()
        device.name = "Plex Web"
        device.product = "Plex Web"
        device.platform = "Web"
        device.clientIdentifier = "device-1"

        account = MagicMock()
        account.devices.return_value = [device]

        server = MagicMock()
        server.myPlexAccount.return_value = account

        result = demo.execute(server=server, params={})

        assert "devices" in result
        assert result["devices"][0]["name"] == "Plex Web"
