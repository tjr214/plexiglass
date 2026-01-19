"""
List Artists demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListArtistsDemo(BaseDemo):
    """List artists in a music library section."""

    name = "List Artists"
    description = "List artists in a specific music library section"
    category = "Media Operations"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "section_name",
                "type": "str",
                "required": True,
                "description": "Music library section name (e.g. Music)",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        section_name = "Music"
        if params and params.get("section_name"):
            section_name = str(params["section_name"])
        return (
            """# List artists
section = server.library.section("""
            f'"{section_name}"' + ")\n"
            "artists = section.all()\n"
            "for artist in artists:\n"
            "    print(artist.title)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        section_name = params.get("section_name")
        if not section_name:
            return {"error": "Missing required parameter: section_name"}

        section = server.library.section(section_name)
        artists = []
        for item in list(section.all()):
            artists.append(
                {
                    "title": getattr(item, "title", "Unknown"),
                    "ratingKey": getattr(item, "ratingKey", None),
                }
            )

        return {"artists": artists}
