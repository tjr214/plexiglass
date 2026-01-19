"""
Get Download URL Demo.

Demonstrates retrieving download URLs for media items.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetDownloadURLDemo(BaseDemo):
    """
    Demonstration of getting download URLs.

    This is a READ operation that retrieves download URLs
    for media items.
    """

    name = "Get Download URL"
    description = "Get download URLs for media files"
    category = "Utilities"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get parameter definitions for this demo.

        Returns:
            List containing title parameter
        """
        return [
            {
                "name": "title",
                "type": "str",
                "required": True,
                "description": "Title of media to get download URL for",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for getting download URLs.

        Args:
            params: Optional parameters

        Returns:
            Python code string demonstrating download URL retrieval
        """
        title = "Avatar"
        if params and params.get("title"):
            title = str(params["title"])

        return f'''# Get download URL for media
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search for media
results = server.search("{title}")
if results:
    item = results[0]
    
    # Get download URL
    download_url = item.getDownloadURL()
    print(f"Download URL: {{download_url}}")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute download URL retrieval.

        Args:
            server: PlexServer instance (or None)
            params: Parameters including 'title'

        Returns:
            Dictionary containing download URL or error
        """
        if server is None:
            return {"error": "No server connection available"}

        title = params.get("title")
        if not title:
            return {"error": "Missing required parameter: title"}

        try:
            # Search for media
            results = server.search(title)
            if not results:
                return {"message": f"No results found for '{title}'"}

            item = results[0]

            # Try to get download URL
            try:
                url = item.getDownloadURL()
                return {
                    "title": getattr(item, "title", title),
                    "url": url,
                    "message": f"Download URL for '{getattr(item, 'title', title)}'",
                }
            except AttributeError:
                return {
                    "message": "Download URL not available for this item type",
                    "info": "Only downloadable media items have download URLs",
                }

        except Exception as e:
            return {"error": f"Failed to get download URL: {str(e)}"}
