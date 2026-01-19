"""
Global Search Demo.

Demonstrates searching across all libraries on the Plex server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GlobalSearchDemo(BaseDemo):
    """
    Demonstration of global search across all Plex libraries.

    This is a READ operation that searches across all media types
    (movies, shows, music, etc.) for a given query string.
    """

    name = "Global Search"
    description = "Search across all libraries for any media"
    category = "Search & Discovery"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get parameter definitions for this demo.

        Returns:
            List containing the query parameter definition
        """
        return [
            {
                "name": "query",
                "type": "str",
                "required": True,
                "description": "Search query string",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for global search.

        Args:
            params: Optional parameters to customize the example

        Returns:
            Python code string demonstrating global search
        """
        query = "Alien"
        if params and params.get("query"):
            query = str(params["query"])

        return f'''# Global search across all libraries
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search across all libraries
results = server.search("{query}")

# Display results
for item in results:
    print(f"{{item.title}} ({{item.type}})")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute global search on the server.

        Args:
            server: PlexServer instance (or None)
            params: Parameters including 'query'

        Returns:
            Dictionary containing search results or error
        """
        if server is None:
            return {"error": "No server connection available"}

        query = params.get("query")
        if not query:
            return {"error": "Missing required parameter: query"}

        try:
            # Execute global search
            search_results = server.search(query)

            # Format results
            results = []
            for item in search_results:
                results.append(
                    {
                        "title": getattr(item, "title", "Unknown"),
                        "type": getattr(item, "type", None),
                        "ratingKey": getattr(item, "ratingKey", None),
                    }
                )

            return {"results": results}

        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}
