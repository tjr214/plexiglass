"""
List Shows demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListShowsDemo(BaseDemo):
    """List shows in a library section."""

    name = "List Shows"
    description = "List shows in a specific library section"
    category = "Media Operations"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "section_name",
                "type": "str",
                "required": True,
                "description": "Show library section name (e.g. TV Shows)",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        section_name = "TV Shows"
        if params and params.get("section_name"):
            section_name = str(params["section_name"])
        return (
            """# List shows
section = server.library.section("""
            f'"{section_name}"' + ")\n"
            "shows = section.all()\n"
            "for show in shows:\n"
            "    print(show.title)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        section_name = params.get("section_name")
        if not section_name:
            return {"error": "Missing required parameter: section_name"}

        section = server.library.section(section_name)
        shows = []
        for item in list(section.all()):
            shows.append(
                {
                    "title": getattr(item, "title", "Unknown"),
                    "ratingKey": getattr(item, "ratingKey", None),
                }
            )

        return {"shows": shows}
