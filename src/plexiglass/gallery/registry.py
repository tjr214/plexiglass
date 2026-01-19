"""
Demo registry for PlexiGlass gallery.

The registry manages all registered gallery demos and provides
discovery methods for finding demos by category, name, etc.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo


class DemoRegistry:
    """
    Registry for managing gallery demos.

    Provides methods to register demos and discover them by
    category, name, or other criteria.
    """

    def __init__(self) -> None:
        """Initialize an empty demo registry."""
        self._demos: list[BaseDemo] = []

    def register(self, demo_class: type[BaseDemo]) -> None:
        """
        Register a demo class in the registry.

        Args:
            demo_class: The demo class to register (not an instance)
        """
        demo_instance = demo_class()
        self._demos.append(demo_instance)

    def register_demo(self, demo_class: type[BaseDemo]) -> type[BaseDemo]:
        """
        Decorator for registering a demo class.

        Usage:
            @registry.register_demo
            class MyDemo(BaseDemo):
                ...

        Args:
            demo_class: The demo class to register

        Returns:
            The demo class (for decorator chaining)
        """
        self.register(demo_class)
        return demo_class

    def get_all_demos(self) -> list[BaseDemo]:
        """
        Get all registered demos.

        Returns:
            List of all demo instances
        """
        return self._demos.copy()

    def get_demos_by_category(self, category: str) -> list[BaseDemo]:
        """
        Get all demos in a specific category.

        Args:
            category: Category name to filter by

        Returns:
            List of demo instances in the category
        """
        return [demo for demo in self._demos if demo.category == category]

    def get_all_categories(self) -> list[str]:
        """
        Get list of all categories that have registered demos.

        Returns:
            List of unique category names
        """
        categories = {demo.category for demo in self._demos}
        return sorted(categories)

    def get_demo_by_name(self, name: str) -> BaseDemo | None:
        """
        Find a demo by its name.

        Args:
            name: Demo name to search for

        Returns:
            Demo instance if found, None otherwise
        """
        for demo in self._demos:
            if demo.name == name:
                return demo
        return None

    def get_demo_count(self) -> int:
        """
        Get total count of registered demos.

        Returns:
            Number of registered demos
        """
        return len(self._demos)

    def get_category_count(self, category: str) -> int:
        """
        Get count of demos in a specific category.

        Args:
            category: Category name

        Returns:
            Number of demos in the category
        """
        return len(self.get_demos_by_category(category))
