"""
List Available Integrations Demo.

Demonstrates listing available integrations and connected devices.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListIntegrationsDemo(BaseDemo):
    """
    Demonstration of listing available integrations.

    This is a READ operation that shows what integrations
    are available or configured on the Plex server.
    """

    name = "List Available Integrations"
    description = "View available integrations and connected devices"
    category = "Integrations"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get parameter definitions for this demo.

        Returns:
            Empty list (no parameters needed)
        """
        return []

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for listing integrations.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating integration listing
        """
        return """# List available integrations
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Plex supports various integrations:
# - Sonos speakers
# - Webhooks
# - Third-party devices

# List connected clients (includes integrations)
clients = server.clients()

print("Connected clients and devices:")
for client in clients:
    print(f"  {client.title} ({client.product})")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute integration listing.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing integration information
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get connected clients (includes integration devices)
            clients = server.clients()

            integrations = []
            for client in clients:
                integrations.append(
                    {
                        "name": getattr(client, "title", "Unknown"),
                        "product": getattr(client, "product", "Unknown"),
                        "type": getattr(client, "protocolCapabilities", ["Unknown"])[0]
                        if hasattr(client, "protocolCapabilities")
                        else "Unknown",
                    }
                )

            return {
                "message": "Available integrations via connected clients",
                "info": {
                    "supported": ["Sonos", "Webhooks", "Third-party apps"],
                    "note": "Integrations appear as connected clients",
                },
                "integrations": integrations,
                "count": len(integrations),
            }

        except Exception as e:
            return {"error": f"Failed to list integrations: {str(e)}"}
