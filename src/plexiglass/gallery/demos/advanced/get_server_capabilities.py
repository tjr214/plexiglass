"""
Get Server Capabilities Demo.

Demonstrates retrieving server capabilities and features.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetServerCapabilitiesDemo(BaseDemo):
    """
    Demonstration of server capabilities discovery.

    This is a READ operation that retrieves information about
    server features and capabilities.
    """

    name = "Get Server Capabilities"
    description = "Discover server capabilities and supported features"
    category = "Advanced Features"
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
        Provide code example for capabilities discovery.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating capabilities discovery
        """
        return """# Get server capabilities
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Server capabilities
print(f"Server Version: {server.version}")
print(f"Platform: {server.platform}")
print(f"Platform Version: {server.platformVersion}")
print(f"Transcoder: {server.transcoderActiveVideoSessions}/{server.transcoderVideoQualities}")

# Check capabilities
print(f"\\nCapabilities:")
if hasattr(server, 'protocolCapabilities'):
    for cap in server.protocolCapabilities:
        print(f"  - {cap}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute capabilities discovery.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing capabilities information or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get server capabilities
            capabilities = {
                "version": getattr(server, "version", "unknown"),
                "platform": getattr(server, "platform", "unknown"),
                "platformVersion": getattr(server, "platformVersion", "unknown"),
                "myPlexSigninState": getattr(server, "myPlexSigninState", "unknown"),
                "transcoderActiveVideoSessions": getattr(
                    server, "transcoderActiveVideoSessions", 0
                ),
            }

            # Get protocol capabilities if available
            if hasattr(server, "protocolCapabilities"):
                capabilities["protocolCapabilities"] = server.protocolCapabilities

            return {
                "info": "Server capabilities and features",
                "capabilities": capabilities,
                "features": ["Transcoding", "Remote Access", "Library Management", "API Access"],
            }

        except Exception as e:
            return {"error": f"Failed to get capabilities: {str(e)}"}
