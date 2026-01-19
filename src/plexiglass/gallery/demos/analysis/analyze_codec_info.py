"""
Analyze Codec Info Demo.

Demonstrates codec analysis for media items.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class AnalyzeCodecInfoDemo(BaseDemo):
    """
    Demonstration of codec information analysis.

    This is a READ operation that provides detailed codec information
    for video and audio streams.
    """

    name = "Analyze Codec Info"
    description = "Get detailed codec information for media files"
    category = "Media Analysis"
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
                "description": "Title of media item to analyze",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for codec analysis.

        Args:
            params: Optional parameters

        Returns:
            Python code string demonstrating codec analysis
        """
        title = "The Matrix"
        if params and params.get("title"):
            title = str(params["title"])

        return f'''# Analyze codecs
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search for media
results = server.search("{title}")
if results:
    item = results[0]
    
    # Get codec information
    for media in item.media:
        print(f"Container: {{media.container}}")
        print(f"Video Codec: {{media.videoCodec}}")
        print(f"Audio Codec: {{media.audioCodec}}")
        print(f"Resolution: {{media.videoResolution}}")
        print(f"Bitrate: {{media.bitrate}}")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute codec analysis.

        Args:
            server: PlexServer instance (or None)
            params: Parameters including 'title'

        Returns:
            Dictionary containing codec information or error
        """
        if server is None:
            return {"error": "No server connection available"}

        title = params.get("title")
        if not title:
            return {"error": "Missing required parameter: title"}

        try:
            # Search for media item
            results = server.search(title)
            if not results:
                return {"message": f"No results found for '{title}'"}

            item = results[0]

            # Analyze codecs
            codecs = []
            for media in getattr(item, "media", []):
                codecs.append(
                    {
                        "container": getattr(media, "container", "unknown"),
                        "videoCodec": getattr(media, "videoCodec", None),
                        "audioCodec": getattr(media, "audioCodec", None),
                        "resolution": getattr(media, "videoResolution", None),
                        "bitrate": getattr(media, "bitrate", None),
                    }
                )

            return {
                "title": getattr(item, "title", title),
                "info": f"Codec analysis for '{getattr(item, 'title', title)}'",
                "codecs": codecs,
            }

        except Exception as e:
            return {"error": f"Failed to analyze codecs: {str(e)}"}
