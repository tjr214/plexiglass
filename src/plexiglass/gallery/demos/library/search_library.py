"""
Search Library demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class SearchLibraryDemo(BaseDemo):
    """Search library items by query."""

    name = "Search Library"
    description = "Search across library items by query"
    category = "Library Management"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "query",
                "type": "str",
                "required": True,
                "description": "Search query",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        query = "Alien"
        if params and params.get("query"):
            query = str(params["query"])
        return (
            """# Search library
results = server.library.search("""
            f'"{query}"' + ")\n"
            "for item in results:\n"
            "    print(item.title, item.type)\n"
        )

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        query = params.get("query")
        if not query:
            return {"error": "Missing required parameter: query"}

        results = []
        for item in list(server.library.search(query)):
            results.append(
                {
                    "title": getattr(item, "title", "Unknown"),
                    "type": getattr(item, "type", None),
                    "ratingKey": getattr(item, "ratingKey", None),
                }
            )

        return {"results": results}
