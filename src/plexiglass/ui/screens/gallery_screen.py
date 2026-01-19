"""
Gallery Screen - Main UI for browsing and executing demos.

This screen provides the interface for navigating through demo categories,
selecting demos, viewing code examples, and executing demonstrations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo
    from plexiglass.gallery.registry import DemoRegistry


class CategoryList(Static):
    """Widget displaying available demo categories."""

    def __init__(self, categories: list[str], **kwargs) -> None:
        """
        Initialize category list.

        Args:
            categories: List of category names to display
        """
        super().__init__(**kwargs)
        self.categories = categories
        self.add_class("category-list")

    def render(self) -> str:
        """Render the category list."""
        if not self.categories:
            return "No categories available"

        lines = ["📚 Gallery Categories:", ""]
        for i, category in enumerate(self.categories, 1):
            lines.append(f"{i}. {category}")

        return "\n".join(lines)


class DemoPanel(Static):
    """Widget displaying selected demo information."""

    def __init__(self, **kwargs) -> None:
        """Initialize demo panel."""
        super().__init__(**kwargs)
        self.current_demo: BaseDemo | None = None
        self.add_class("demo-panel")

    def set_demo(self, demo: BaseDemo | None) -> None:
        """
        Set the currently displayed demo.

        Args:
            demo: Demo to display, or None to clear
        """
        self.current_demo = demo
        self.update(self.render())

    def render(self) -> str:
        """Render the demo panel."""
        if self.current_demo is None:
            return "Select a category and demo to view details"

        lines = [
            f"📋 {self.current_demo.name}",
            "",
            f"Description: {self.current_demo.description}",
            f"Category: {self.current_demo.category}",
            f"Type: {self.current_demo.operation_type}",
        ]

        return "\n".join(lines)


class GalleryScreen(Screen):
    """
    Screen for browsing and executing API gallery demos.

    The Gallery Screen provides:
    - Category navigation
    - Demo selection
    - Code examples
    - Demo execution
    - Results display
    """

    TITLE = "PlexiGlass API Gallery"
    CSS_PATH = "../styles/gallery.tcss"
    BINDINGS = [
        ("escape", "dismiss", "Back to Dashboard"),
        ("q", "dismiss", "Quit Gallery"),
    ]

    def __init__(self, registry: DemoRegistry, **kwargs) -> None:
        """
        Initialize the Gallery Screen.

        Args:
            registry: DemoRegistry instance containing all demos
        """
        super().__init__(**kwargs)
        self.registry = registry
        self._selected_category: str | None = None
        self._selected_demo: BaseDemo | None = None

    @property
    def selected_category(self) -> str | None:
        """Get the currently selected category."""
        return self._selected_category

    @selected_category.setter
    def selected_category(self, category: str | None) -> None:
        """Set the currently selected category."""
        self._selected_category = category

    @property
    def selected_demo(self) -> BaseDemo | None:
        """Get the currently selected demo."""
        return self._selected_demo

    @selected_demo.setter
    def selected_demo(self, demo: BaseDemo | None) -> None:
        """Set the currently selected demo."""
        self._selected_demo = demo
        # Update the demo panel if it exists
        try:
            demo_panel = self.query_one("#demo-panel", DemoPanel)
            demo_panel.set_demo(demo)
        except Exception:
            # Panel might not be composed yet
            pass

    def get_current_demos(self) -> list[BaseDemo]:
        """
        Get demos for the currently selected category.

        Returns:
            List of demos in the selected category
        """
        if self._selected_category is None:
            return []
        return self.registry.get_demos_by_category(self._selected_category)

    def compose(self) -> ComposeResult:
        """Compose the Gallery Screen layout."""
        yield Header()

        # Main container with sidebar and content area
        with Horizontal(id="gallery-container"):
            # Category sidebar
            categories = self.registry.get_all_categories()
            yield CategoryList(categories, id="category-list")

            # Demo panel
            yield DemoPanel(id="demo-panel")

        yield Footer()

    async def action_dismiss(self, result=None) -> None:
        """Dismiss the gallery screen."""
        self.app.pop_screen()
