"""
CategoryMenu widget for PlexiGlass Gallery.

Provides interactive navigation through gallery demo categories with counts and emojis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

if TYPE_CHECKING:
    from plexiglass.gallery.registry import DemoRegistry


class CategoryMenu(VerticalScroll):
    """
    Widget for navigating demo categories.

    Displays all available categories from the registry with:
    - Category emoji icon
    - Category name
    - Demo count
    - Interactive selection
    """

    DEFAULT_CSS = """
    CategoryMenu {
        border: round $primary;
        background: $panel;
        padding: 1;
        width: 30;
        height: 100%;
    }

    CategoryMenu > ListView {
        background: transparent;
        border: none;
    }

    CategoryMenu > ListView > ListItem {
        padding: 0 1;
        height: auto;
    }

    CategoryMenu > ListView > ListItem:hover {
        background: $primary-darken-2;
    }

    CategoryMenu > ListView > ListItem.-selected {
        background: $primary;
        color: $text;
    }

    CategoryMenu Label {
        color: $text-muted;
        text-align: center;
        padding: 2;
    }
    """

    # Emoji mapping for categories
    CATEGORY_EMOJIS = {
        "Server & Connection": "📡",
        "Library Management": "📚",
        "Media Operations": "🎬",
        "Playback & Clients": "🎮",
        "Collections & Playlists": "📦",
        "Users & Sharing": "👥",
        "MyPlex Account": "👤",
        "Settings & Preferences": "⚙️",
        "Search & Discovery": "🔍",
        "Sync & Offline": "📱",
        "Alerts & Monitoring": "🔔",
        "Integrations": "🔊",
        "Media Analysis": "🔬",
        "Utilities": "🛠️",
        "Advanced Features": "🧪",
    }

    class CategorySelected(Message):
        """Message emitted when a category is selected."""

        def __init__(self, category: str) -> None:
            """
            Initialize CategorySelected message.

            Args:
                category: Name of the selected category
            """
            super().__init__()
            self.category = category

    def __init__(self, registry: DemoRegistry, **kwargs) -> None:
        """
        Initialize CategoryMenu.

        Args:
            registry: DemoRegistry instance containing all demos
        """
        super().__init__(**kwargs)
        self.registry = registry
        self.selected_category: str | None = None
        self._category_map: dict[int, str] = {}  # Maps list item index to category
        self.add_class("category-menu")

    def get_categories(self) -> list[str]:
        """
        Get list of all categories from the registry.

        Returns:
            Sorted list of category names
        """
        return self.registry.get_all_categories()

    def get_category_emoji(self, category: str) -> str:
        """
        Get emoji icon for a category.

        Args:
            category: Category name

        Returns:
            Emoji string for the category, or default emoji if not found
        """
        return self.CATEGORY_EMOJIS.get(category, "📋")

    def format_category_display(self, category: str) -> str:
        """
        Format category display string with emoji and demo count.

        Args:
            category: Category name

        Returns:
            Formatted string like "📡 Server & Connection (5)"
        """
        emoji = self.get_category_emoji(category)
        count = self.registry.get_category_count(category)
        return f"{emoji} {category} ({count})"

    def select_category(self, category: str) -> None:
        """
        Set the selected category and emit message.

        Args:
            category: Category name to select
        """
        self.selected_category = category
        self.post_message(self.CategorySelected(category))

    def compose(self) -> ComposeResult:
        """
        Compose the CategoryMenu layout.

        Yields:
            ListView with pre-populated ListItems for each category
        """
        categories = self.get_categories()

        if not categories:
            yield Label("No categories available")
            return

        # Yield the ListView with initial items
        yield ListView(*self._create_list_items(categories), id="category-list-view")

    def _create_list_items(self, categories: list[str]) -> list[ListItem]:
        """
        Create ListItem widgets for categories.

        Args:
            categories: List of category names

        Returns:
            List of ListItem widgets
        """
        items = []
        for index, category in enumerate(categories):
            display_text = self.format_category_display(category)
            list_item = ListItem(Label(display_text))
            # Map the item index to the category name
            self._category_map[index] = category
            items.append(list_item)
        return items

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Handle category selection from ListView.

        Args:
            event: ListView.Selected event
        """
        # Get the category from our mapping using the list item's index
        list_view = event.list_view
        index = list_view.index
        if index is not None and index in self._category_map:
            category = self._category_map[index]
            self.select_category(category)
