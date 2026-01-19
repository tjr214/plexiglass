"""
Tests for ListServerClientsDemo.
"""

from __future__ import annotations

from unittest.mock import MagicMock

from plexiglass.gallery.demos.server.list_server_clients import ListServerClientsDemo


class TestListServerClientsDemo:
    """Unit tests for ListServerClientsDemo."""

    def test_demo_metadata(self):
        demo = ListServerClientsDemo()

        assert demo.name == "List Server Clients"
        assert demo.category == "Server & Connection"
        assert demo.operation_type == "READ"

    def test_demo_code_example(self):
        demo = ListServerClientsDemo()
        code = demo.get_code_example()

        assert "clients" in code

    def test_demo_execute_with_none_server(self):
        demo = ListServerClientsDemo()

        result = demo.execute(server=None, params={})

        assert "error" in result

    def test_demo_execute_returns_clients(self):
        demo = ListServerClientsDemo()

        client = MagicMock()
        client.title = "Living Room"
        client.device = "Roku"
        client.platform = "Roku"
        client.version = "1.2.3"
        client.machineIdentifier = "client-123"

        server = MagicMock()
        server.clients.return_value = [client]

        result = demo.execute(server=server, params={})

        assert "clients" in result
        assert result["clients"][0]["title"] == "Living Room"
        assert result["clients"][0]["platform"] == "Roku"
