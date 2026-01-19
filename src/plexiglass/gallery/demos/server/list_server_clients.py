"""
List Server Clients demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListServerClientsDemo(BaseDemo):
    """List clients connected to the server."""

    name = "List Server Clients"
    description = "List active clients connected to the server"
    category = "Server & Connection"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List active clients
clients = server.clients()
for client in clients:
    print(client.title, client.platform)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        clients = []
        for client in list(server.clients()):
            clients.append(
                {
                    "title": getattr(client, "title", "Unknown"),
                    "device": getattr(client, "device", None),
                    "platform": getattr(client, "platform", None),
                    "version": getattr(client, "version", None),
                    "machineIdentifier": getattr(client, "machineIdentifier", None),
                }
            )

        return {"clients": clients}
