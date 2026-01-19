"""
Discover Sonos Speakers Demo.

Demonstrates Sonos speaker discovery via Plex.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class DiscoverSonosDemo(BaseDemo):
    """
    Demonstration of Sonos speaker discovery.

    This is a READ operation that shows available Sonos speakers
    connected to the Plex server.
    """

    name = "Discover Sonos Speakers"
    description = "Discover Sonos speakers connected to Plex"
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
        Provide code example for Sonos discovery.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating Sonos discovery
        """
        return """# Discover Sonos speakers
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Sonos integration via plexapi
# Note: Requires plexapi.sonos module

try:
    from plexapi.sonos import SonosSpeaker
    
    # Discover Sonos speakers
    speakers = SonosSpeaker.discover()
    
    for speaker in speakers:
        print(f"Speaker: {speaker.name}")
        print(f"  Model: {speaker.model}")
except ImportError:
    print("Sonos integration requires plexapi.sonos module")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute Sonos discovery.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing Sonos speaker information or message
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Try to import sonos module
            try:
                from plexapi.sonos import SonosSpeaker

                # Attempt discovery (may timeout or fail if no Sonos devices)
                speakers = SonosSpeaker.discover()

                if speakers:
                    results = []
                    for speaker in speakers:
                        results.append(
                            {
                                "name": getattr(speaker, "name", "Unknown"),
                                "model": getattr(speaker, "model", "Unknown"),
                            }
                        )
                    return {"speakers": results}
                else:
                    return {"message": "No Sonos speakers discovered", "speakers": []}

            except ImportError:
                return {
                    "info": "Sonos integration requires the plexapi.sonos module",
                    "message": "Install plexapi with Sonos support for this feature",
                }

        except Exception as e:
            return {
                "message": f"Sonos discovery not available: {str(e)}",
                "info": "Sonos integration may not be configured on this server",
            }
