"""
Hub Search Demo - Search content hubs (trending, popular, etc.).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class HubSearchDemo(BaseDemo):
    """
    Demonstration of searching Plex content hubs.

    Hubs provide curated content like "Trending", "Popular", "Recently Added", etc.
    This is a READ operation.
    """

    name = "Hub Search"
    description = "Browse content hubs like Trending and Popular"
    category = "Search & Discovery"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """Get parameter definitions for this demo."""
        return []

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """Provide code example for hub search."""
        return """# Browse content hubs
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Get all hubs
hubs = server.library.hubs()

# Display hub information
for hub in hubs:
    print(f"Hub: {hub.title}")
    print(f"  Type: {hub.type}")
    print(f"  Size: {hub.size}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """Execute hub search on the server."""
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get hubs from the library
            hubs = server.library.hubs()

            # Format results
            results = []
            for hub in hubs:
                results.append(
                    {
                        "title": getattr(hub, "title", "Unknown"),
                        "type": getattr(hub, "type", None),
                        "size": getattr(hub, "size", 0),
                    }
                )

            return {"hubs": results}

        except Exception as e:
            return {"error": f"Hub search failed: {str(e)}"}
