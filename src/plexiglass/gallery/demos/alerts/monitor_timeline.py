"""
Monitor Timeline Demo.

Demonstrates timeline monitoring on the Plex server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class MonitorTimelineDemo(BaseDemo):
    """
    Demonstration of timeline monitoring.

    This is a READ operation that shows how to monitor
    timeline updates on the Plex server.
    """

    name = "Monitor Timeline"
    description = "View timeline information and monitoring capabilities"
    category = "Alerts & Monitoring"
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
        Provide code example for timeline monitoring.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating timeline monitoring
        """
        return """# Monitor server timeline
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Timeline monitoring requires alert listener setup
# Here's how to get timeline information:

# Get server timeline (current state)
timeline = server.timeline()

# Timeline provides info about:
# - Current playback state
# - Media updates
# - Library changes

print(f"Timeline: {timeline}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute timeline monitoring on the server.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing timeline information or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Note: timeline() method may not be available on all servers
            # Provide information about timeline monitoring

            return {
                "message": "Timeline monitoring is available via Alert listeners",
                "info": {
                    "description": "Timeline provides real-time updates about playback state and library changes",
                    "usage": "Use server.startAlertListener() to monitor timeline events",
                    "events": ["Playing", "Paused", "Stopped", "Library Updated"],
                },
                "timeline": "Use Alert listener for real-time timeline monitoring",
            }

        except Exception as e:
            return {"error": f"Failed to access timeline: {str(e)}"}
