"""
List Playlists demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListPlaylistsDemo(BaseDemo):
    """List playlists on the server."""

    name = "List Playlists"
    description = "List playlists available on the server"
    category = "Collections & Playlists"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List playlists
playlists = server.playlists()
for playlist in playlists:
    print(playlist.title, playlist.playlistType)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        playlists = []
        for playlist in list(server.playlists()):
            playlists.append(
                {
                    "title": getattr(playlist, "title", "Unknown"),
                    "playlist_type": getattr(playlist, "playlistType", None),
                    "ratingKey": getattr(playlist, "ratingKey", None),
                }
            )

        return {"playlists": playlists}
