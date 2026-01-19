"""
Get Thumbnail URL Demo.

Demonstrates retrieving thumbnail and artwork URLs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetThumbnailURLDemo(BaseDemo):
    """
    Demonstration of getting thumbnail URLs.

    This is a READ operation that retrieves thumbnail
    and artwork URLs for media items.
    """

    name = "Get Thumbnail URL"
    description = "Get thumbnail and artwork URLs for media"
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
                "description": "Title of media to get thumbnails for",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for getting thumbnail URLs.

        Args:
            params: Optional parameters

        Returns:
            Python code string demonstrating thumbnail URL retrieval
        """
        title = "The Matrix"
        if params and params.get("title"):
            title = str(params["title"])

        return f'''# Get thumbnail URLs
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search for media
results = server.search("{title}")
if results:
    item = results[0]
    
    # Get full URLs
    thumb_url = server.url(item.thumb, includeToken=True)
    art_url = server.url(item.art, includeToken=True)
    
    print(f"Thumbnail: {{thumb_url}}")
    print(f"Art: {{art_url}}")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute thumbnail URL retrieval.

        Args:
            server: PlexServer instance (or None)
            params: Parameters including 'title'

        Returns:
            Dictionary containing thumbnail URLs or error
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

            # Get thumbnail and art paths
            thumb = getattr(item, "thumb", None)
            art = getattr(item, "art", None)

            result = {
                "title": getattr(item, "title", title),
            }

            if thumb:
                result["thumb"] = thumb
                result["thumb_full"] = f"{server.url('')}{thumb}"

            if art:
                result["art"] = art
                result["art_full"] = f"{server.url('')}{art}"

            if not thumb and not art:
                result["message"] = "No thumbnails available for this item"

            return result

        except Exception as e:
            return {"error": f"Failed to get thumbnail URLs: {str(e)}"}
