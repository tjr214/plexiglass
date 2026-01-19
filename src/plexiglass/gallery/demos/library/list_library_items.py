"""
List Library Items demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class ListLibraryItemsDemo(BaseDemo):
    """List items in a library section."""

    name = "List Library Items"
    description = "List items in a specific library section"
    category = "Library Management"
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
            """# List items in a library section
section = server.library.section("""
            f'"{section_name}"' + ")\n"
            "items = section.all()\n"
            "for item in items:\n"
            "    print(item.title, item.type)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        section_name = params.get("section_name")
        if not section_name:
            return {"error": "Missing required parameter: section_name"}

        section = server.library.section(section_name)
        items = []
        for item in list(section.all()):
            items.append(
                {
                    "title": getattr(item, "title", "Unknown"),
                    "type": getattr(item, "type", None),
                    "ratingKey": getattr(item, "ratingKey", None),
                }
            )

        return {"items": items}
