"""
List Sync Items Demo.

Demonstrates listing all sync items configured on the Plex server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListSyncItemsDemo(BaseDemo):
    """
    Demonstration of listing sync items on a Plex server.

    This is a READ operation that retrieves all configured sync items
    for offline playback across devices.
    """

    name = "List Sync Items"
    description = "View all sync items configured for offline playback"
    category = "Sync & Offline"
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
        Provide code example for listing sync items.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating sync items listing
        """
        return """# List all sync items
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Get all sync items
sync_items = server.syncItems()

# Display sync items
for item in sync_items:
    print(f"{item.title} - Status: {item.status}")
    print(f"  Device: {item.clientIdentifier}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute sync items listing on the server.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing sync items or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get all sync items
            sync_items = server.syncItems()

            # Format results
            results = []
            for item in sync_items:
                results.append(
                    {
                        "title": getattr(item, "title", "Unknown"),
                        "status": getattr(item, "status", "Unknown"),
                        "clientIdentifier": getattr(item, "clientIdentifier", None),
                    }
                )

            return {"sync_items": results}

        except Exception as e:
            return {"error": f"Failed to list sync items: {str(e)}"}
