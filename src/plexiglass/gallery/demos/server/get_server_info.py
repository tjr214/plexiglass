"""
Get Server Info Demo - Proof of Concept Gallery Demo.

This demo retrieves basic information from a Plex Media Server,
demonstrating the BaseDemo pattern and python-plexapi usage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetServerInfoDemo(BaseDemo):
    """
    Demonstration of retrieving basic server information.

    This is a READ operation that safely queries the server for
    basic information like name, version, and platform details.
    """

    name = "Get Server Info"
    description = "Retrieve basic server information and status"
    category = "Server & Connection"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """
        Provide code example for getting server information.

        Args:
            params: Optional parameters (not used in this demo)

        Returns:
            Python code string demonstrating the API usage
        """
        return """# Connect to Plex server and get basic info
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Get server information
print(f"Server Name: {server.friendlyName}")
print(f"Version: {server.version}")
print(f"Platform: {server.platform}")
print(f"Platform Version: {server.platformVersion}")
print(f"Machine ID: {server.machineIdentifier}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the demo to retrieve server information.

        Args:
            server: PlexServer instance (or None)
            params: Parameters for the demo (not used)

        Returns:
            Dictionary containing server information or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Retrieve server properties
            result = {
                "friendlyName": server.friendlyName,
                "version": server.version,
                "platform": server.platform,
                "platformVersion": server.platformVersion,
                "machineIdentifier": server.machineIdentifier,
            }
            return result
        except Exception as e:
            return {"error": f"Failed to retrieve server info: {str(e)}"}

    def get_parameters(self) -> list[dict[str, Any]]:
        """
        Get parameter definitions for this demo.

        This demo requires no parameters.

        Returns:
            Empty list (no parameters needed)
        """
        return []
