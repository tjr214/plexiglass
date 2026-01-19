"""
List Collections demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListCollectionsDemo(BaseDemo):
    """List collections for a library section."""

    name = "List Collections"
    description = "List collections in a library section"
    category = "Collections & Playlists"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "section_name",
                "type": "str",
                "required": True,
                "description": "Library section name (e.g. Movies)",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        section_name = "Movies"
        if params and params.get("section_name"):
            section_name = str(params["section_name"])
        return (
            """# List collections
section = server.library.section("""
            f'"{section_name}"' + ")\n"
            "collections = section.collections()\n"
            "for collection in collections:\n"
            "    print(collection.title)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        section_name = params.get("section_name")
        if not section_name:
            return {"error": "Missing required parameter: section_name"}

        section = server.library.section(section_name)
        collections = []
        for collection in list(section.collections()):
            collections.append(
                {
                    "title": getattr(collection, "title", "Unknown"),
                    "ratingKey": getattr(collection, "ratingKey", None),
                }
            )

        return {"collections": collections}
