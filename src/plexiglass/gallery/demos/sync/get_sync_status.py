"""
Get Sync Status Demo.

Demonstrates retrieving sync status summary from the Plex server.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetSyncStatusDemo(BaseDemo):
    """
    Demonstration of getting sync status summary.

    This is a READ operation that retrieves a summary of all
    sync operations and their current status.
    """

    name = "Get Sync Status"
    description = "Get summary of sync operations and their status"
    category = "Sync & Offline"
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
        Provide code example for getting sync status.

        Args:
            params: Optional parameters (not used)

        Returns:
            Python code string demonstrating sync status retrieval
        """
        return """# Get sync status summary
from plexapi.server import PlexServer
from collections import Counter

# Initialize connection
server = PlexServer(baseurl, token)

# Get all sync items
sync_items = server.syncItems()

# Count statuses
status_counts = Counter(item.status for item in sync_items)

# Display summary
print(f"Total sync items: {len(sync_items)}")
for status, count in status_counts.items():
    print(f"  {status}: {count}")
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """
        Execute sync status retrieval on the server.

        Args:
            server: PlexServer instance (or None)
            params: Parameters (not used)

        Returns:
            Dictionary containing sync status summary or error
        """
        if server is None:
            return {"error": "No server connection available"}

        try:
            # Get all sync items
            sync_items = server.syncItems()

            # Count statuses
            status_counts = {}
            for item in sync_items:
                status = getattr(item, "status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1

            # Create summary
            summary = {
                "total": len(sync_items),
                "complete": status_counts.get("complete", 0),
                "processing": status_counts.get("processing", 0),
                "pending": status_counts.get("pending", 0),
                "failed": status_counts.get("failed", 0),
            }

            return {"status_summary": summary}

        except Exception as e:
            return {"error": f"Failed to get sync status: {str(e)}"}
