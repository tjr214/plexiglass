"""
Get Recommendations Demo - Get recommended content based on an item.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class GetRecommendationsDemo(BaseDemo):
    """
    Demonstration of getting recommendations for media items.

    Shows related/similar content based on a given item.
    This is a READ operation.
    """

    name = "Get Recommendations"
    description = "Get recommended/similar content for an item"
    category = "Search & Discovery"
    operation_type = "READ"

    def get_parameters(self) -> list[dict[str, Any]]:
        """Get parameter definitions for this demo."""
        return [
            {
                "name": "title",
                "type": "str",
                "required": True,
                "description": "Title of item to get recommendations for",
            }
        ]

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        """Provide code example for getting recommendations."""
        title = "The Matrix"
        if params and params.get("title"):
            title = str(params["title"])

        return f'''# Get recommendations for an item
from plexapi.server import PlexServer

# Initialize connection
server = PlexServer(baseurl, token)

# Search for the item
items = server.library.search("{title}")
if items:
    item = items[0]
    
    # Get similar/related items
    similar = item.similar()
    
    # Display recommendations
    for rec in similar:
        print(f"{{rec.title}} ({{rec.year}})")
'''

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        """Execute recommendations demo."""
        if server is None:
            return {"error": "No server connection available"}

        title = params.get("title")
        if not title:
            return {"error": "Missing required parameter: title"}

        try:
            # Search for the item
            search_results = server.library.search(title)

            if not search_results:
                return {"error": f"No items found for '{title}'"}

            # Get the first result
            item = search_results[0]

            # Get similar items
            similar_items = item.similar()

            # Format results
            results = []
            for sim_item in similar_items:
                results.append(
                    {
                        "title": getattr(sim_item, "title", "Unknown"),
                        "year": getattr(sim_item, "year", None),
                        "type": getattr(sim_item, "type", None),
                        "ratingKey": getattr(sim_item, "ratingKey", None),
                    }
                )

            return {"source_item": getattr(item, "title", "Unknown"), "recommendations": results}

        except Exception as e:
            return {"error": f"Failed to get recommendations: {str(e)}"}
