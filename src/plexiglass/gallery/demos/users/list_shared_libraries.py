"""
List Shared Libraries demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListSharedLibrariesDemo(BaseDemo):
    """List shared libraries for the Plex account."""

    name = "List Shared Libraries"
    description = "List libraries shared with the Plex account"
    category = "Users & Sharing"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List shared libraries
account = server.myPlexAccount()
for share in account.sharedLibraries():
    print(share.title, share.sections)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        account = server.myPlexAccount()
        shares = []
        for share in list(account.sharedLibraries()):
            shares.append(
                {
                    "title": getattr(share, "title", "Unknown"),
                    "sections": getattr(share, "sections", []),
                }
            )

        return {"shared_libraries": shares}
