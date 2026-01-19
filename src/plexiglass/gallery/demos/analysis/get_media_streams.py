"""
Get Media Streams Demo.

Demonstrates retrieving detailed stream information from media items.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetMediaStreamsDemo(BaseDemo):
    """
    Demonstration of media stream analysis.

    This is a READ operation that retrieves detailed information about
    video, audio, and subtitle streams in media files.
    """

    name = "Get Media Streams"
    description = "Analyze video, audio, and subtitle streams in media files"
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
        Provide code example for stream analysis.

        Args:
            params: Optional parameters

        Returns:
            Python code string demonstrating stream analysis
        """
        title = "Inception"
        if params and params.get("title"):
            title = str(params["title"])

        return f'''# Analyze media streams
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search for media item
results = server.search("{title}")
if results:
    item = results[0]
    
    # Access media streams
    for media in item.media:
        print(f"Media: {{media.videoResolution}} {{media.audioCodec}}")
        
        for part in media.parts:
            for stream in part.streams:
                if stream.streamType == 1:  # Video
                    print(f"  Video: {{stream.codec}} {{stream.bitrate}}")
                elif stream.streamType == 2:  # Audio
                    print(f"  Audio: {{stream.codec}} {{stream.channels}}ch")
                elif stream.streamType == 3:  # Subtitle
                    print(f"  Subtitle: {{stream.language}}")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute media stream analysis.

        Args:
            server: PlexServer instance (or None)
            params: Parameters including 'title'

        Returns:
            Dictionary containing stream information or error
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

            # Analyze streams
            all_streams = []
            for media in getattr(item, "media", []):
                for part in getattr(media, "parts", []):
                    for stream in getattr(part, "streams", []):
                        stream_type = getattr(stream, "streamType", 0)
                        type_name = {1: "video", 2: "audio", 3: "subtitle"}.get(
                            stream_type, "unknown"
                        )

                        all_streams.append(
                            {
                                "type": type_name,
                                "codec": getattr(stream, "codec", "unknown"),
                                "language": getattr(stream, "language", None),
                                "bitrate": getattr(stream, "bitrate", None),
                            }
                        )

            return {
                "title": getattr(item, "title", title),
                "streams": all_streams,
                "stream_count": len(all_streams),
            }

        except Exception as e:
            return {"error": f"Failed to analyze streams: {str(e)}"}
