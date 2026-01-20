"""
Lazy Demo Loader for PlexiGlass gallery.

Provides lazy loading of demo instances to prevent upfront
instantiation of all 35 demos at startup.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo


class LazyDemoLoader:
    """
    Lazy loader for gallery demos.

    Defers demo instantiation until actually needed, improving
    startup performance and memory usage.

    Features:
    - Demo class registration without instantiation
    - On-demand demo loading
    - Metadata access without loading demos
    - Statistics tracking

    Example:
        >>> loader = LazyDemoLoader()
        >>> loader.register(MyDemo)
        >>> demo = loader.get_demo("My Demo")  # Loads on access
        >>> print(demo.name)
    """

    def __init__(self) -> None:
        """Initialize an empty lazy demo loader."""
        self._demo_classes: list[type[BaseDemo]] = []
        self._demo_instances: dict[str, BaseDemo] = {}

    def register(self, demo_class: type[BaseDemo]) -> None:
        """
        Register a demo class without instantiating it.

        Args:
            demo_class: The demo class to register (not an instance)
        """
        self._demo_classes.append(demo_class)

    def register_demo(self, demo_class: type[BaseDemo]) -> type[BaseDemo]:
        """
        Decorator for registering a demo class.

        Usage:
            @loader.register_demo
            class MyDemo(BaseDemo):
                ...

        Args:
            demo_class: The demo class to register

        Returns:
            The demo class (for decorator chaining)
        """
        self.register(demo_class)
        return demo_class

    def get_demo(self, name: str) -> BaseDemo | None:
        """
        Get a demo by name, loading it if not already loaded.

        Args:
            name: Demo name to retrieve

        Returns:
            Demo instance if found, None otherwise
        """
        # Check if already loaded
        if name in self._demo_instances:
            return self._demo_instances[name]

        # Find and load the demo
        for demo_class in self._demo_classes:
            if demo_class.name == name:
                instance = demo_class()
                self._demo_instances[name] = instance
                return instance

        return None

    def get_demo_by_name(self, name: str) -> BaseDemo | None:
        """
        Find a demo by its name.

        Alias for get_demo() for compatibility with DemoRegistry.

        Args:
            name: Demo name to search for

        Returns:
            Demo instance if found, None otherwise
        """
        return self.get_demo(name)

    def get_all_demos(self) -> list[BaseDemo]:
        """
        Get all registered demos, loading any not yet loaded.

        Returns:
            List of all demo instances
        """
        # Ensure all demos are loaded
        for demo_class in self._demo_classes:
            if demo_class.name not in self._demo_instances:
                self._demo_instances[demo_class.name] = demo_class()

        return list(self._demo_instances.values())

    def get_demos_by_category(self, category: str) -> list[BaseDemo]:
        """
        Get all demos in a specific category, loading them if needed.

        Args:
            category: Category name to filter by

        Returns:
            List of demo instances in category
        """
        demos = []
        for demo_class in self._demo_classes:
            if demo_class.category == category:
                # Load demo if needed
                if demo_class.name not in self._demo_instances:
                    self._demo_instances[demo_class.name] = demo_class()
                demos.append(self._demo_instances[demo_class.name])
        return demos

    def get_all_categories(self) -> list[str]:
        """
        Get list of all categories that have registered demos.

        This does NOT load any demo instances.

        Returns:
            List of unique category names
        """
        categories = {demo_class.category for demo_class in self._demo_classes}
        return sorted(categories)

    def get_demo_count(self) -> int:
        """
        Get total count of registered demos.

        This does NOT load any demo instances.

        Returns:
            Number of registered demos
        """
        return len(self._demo_classes)

    def get_category_count(self, category: str) -> int:
        """
        Get count of demos in a specific category.

        This does NOT load any demo instances.

        Args:
            category: Category name

        Returns:
            Number of demos in category
        """
        return len(
            [demo_class for demo_class in self._demo_classes if demo_class.category == category]
        )

    def get_registered_count(self) -> int:
        """
        Get number of registered demo classes.

        Returns:
            Number of registered demo classes
        """
        return len(self._demo_classes)

    def get_loaded_count(self) -> int:
        """
        Get number of currently loaded demo instances.

        Returns:
            Number of loaded demo instances
        """
        return len(self._demo_instances)

    def clear_loaded(self) -> None:
        """
        Clear all loaded demo instances while keeping registrations.

        Useful for freeing memory or reinitializing demos.
        """
        self._demo_instances.clear()

    def clear_all(self) -> None:
        """
        Clear all registrations and loaded demos.

        Resets the loader to initial empty state.
        """
        self._demo_classes.clear()
        self._demo_instances.clear()

    def get_statistics(self) -> dict[str, float | int]:
        """
        Get loader statistics.

        Returns:
            Dictionary with statistics:
            - registered: Number of registered demo classes
            - loaded: Number of loaded demo instances
            - load_percentage: Percentage of demos loaded
        """
        registered = len(self._demo_classes)
        loaded = len(self._demo_instances)
        load_percentage = (loaded / registered * 100) if registered > 0 else 0.0

        return {
            "registered": registered,
            "loaded": loaded,
            "load_percentage": load_percentage,
        }
