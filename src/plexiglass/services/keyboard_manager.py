"""
Keyboard Shortcut Manager Service.

Manages keyboard shortcuts across the PlexiGlass application with:
- Global and context-aware shortcuts
- Conflict detection
- Customization support
- Enable/disable functionality
- Help text generation
"""

from dataclasses import dataclass, field
from typing import Optional


class ShortcutConflict(Exception):
    """Exception raised when a keyboard shortcut conflict is detected."""

    pass


@dataclass
class Shortcut:
    """Represents a keyboard shortcut."""

    key: str
    action: str
    description: str
    context: str = "global"
    enabled: bool = True

    def __eq__(self, other):
        """Check equality based on key, action, and context."""
        if not isinstance(other, Shortcut):
            return False
        return (
            self.key == other.key and self.action == other.action and self.context == other.context
        )

    def __repr__(self):
        """String representation of the shortcut."""
        return f"Shortcut(key='{self.key}', action='{self.action}', context='{self.context}')"

    def to_dict(self) -> dict:
        """Convert shortcut to dictionary."""
        return {
            "key": self.key,
            "action": self.action,
            "description": self.description,
            "context": self.context,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Shortcut":
        """Create shortcut from dictionary."""
        return cls(
            key=data["key"],
            action=data["action"],
            description=data["description"],
            context=data.get("context", "global"),
            enabled=data.get("enabled", True),
        )


class KeyboardShortcutManager:
    """
    Manages keyboard shortcuts for PlexiGlass.

    Features:
    - Register/unregister shortcuts
    - Context-aware shortcuts (global, dashboard, gallery, etc.)
    - Conflict detection
    - Enable/disable shortcuts
    - Help text generation
    - Import/export configuration
    """

    def __init__(self):
        """Initialize the keyboard shortcut manager."""
        self._shortcuts: list[Shortcut] = []

    def register(
        self,
        key: str,
        action: str,
        description: str,
        context: str = "global",
        force: bool = False,
    ) -> None:
        """
        Register a new keyboard shortcut.

        Args:
            key: The keyboard shortcut (e.g., "ctrl+s")
            action: The action identifier
            description: Human-readable description
            context: Context where shortcut is active (default: "global")
            force: Override existing shortcut if conflict exists

        Raises:
            ShortcutConflict: If key already registered in same context and force=False
        """
        # Check for conflicts
        if not force and self.has_conflict(key, context):
            raise ShortcutConflict(f"Shortcut '{key}' already registered in context '{context}'")

        # Remove existing if force=True
        if force:
            self._remove_by_key_and_context(key, context)

        # Register new shortcut
        shortcut = Shortcut(
            key=key,
            action=action,
            description=description,
            context=context,
        )
        self._shortcuts.append(shortcut)

    def unregister(self, key: str, context: str = "global") -> None:
        """
        Unregister a keyboard shortcut.

        Args:
            key: The keyboard shortcut to remove
            context: The context to remove from (default: "global")
        """
        self._remove_by_key_and_context(key, context)

    def get_shortcut(self, key: str, context: str = "global") -> Optional[Shortcut]:
        """
        Get a specific shortcut by key and context.

        Args:
            key: The keyboard shortcut
            context: The context (default: "global")

        Returns:
            The shortcut if found, None otherwise
        """
        for shortcut in self._shortcuts:
            if shortcut.key == key and shortcut.context == context:
                return shortcut
        return None

    def get_all_shortcuts(self) -> list[Shortcut]:
        """
        Get all registered shortcuts.

        Returns:
            List of all shortcuts
        """
        return self._shortcuts.copy()

    def get_shortcuts_by_context(self, context: str) -> list[Shortcut]:
        """
        Get all shortcuts for a specific context.

        Args:
            context: The context to filter by

        Returns:
            List of shortcuts in the specified context
        """
        return [s for s in self._shortcuts if s.context == context]

    def get_enabled_shortcuts(self, context: Optional[str] = None) -> list[Shortcut]:
        """
        Get all enabled shortcuts, optionally filtered by context.

        Args:
            context: Optional context to filter by

        Returns:
            List of enabled shortcuts
        """
        shortcuts = self._shortcuts if context is None else self.get_shortcuts_by_context(context)
        return [s for s in shortcuts if s.enabled]

    def has_conflict(self, key: str, context: str = "global") -> bool:
        """
        Check if a shortcut key conflicts with existing registration.

        Args:
            key: The keyboard shortcut to check
            context: The context to check in

        Returns:
            True if conflict exists, False otherwise
        """
        return self.get_shortcut(key, context) is not None

    def enable(self, key: str, context: str = "global") -> None:
        """
        Enable a shortcut.

        Args:
            key: The keyboard shortcut
            context: The context
        """
        shortcut = self.get_shortcut(key, context)
        if shortcut:
            shortcut.enabled = True

    def disable(self, key: str, context: str = "global") -> None:
        """
        Disable a shortcut.

        Args:
            key: The keyboard shortcut
            context: The context
        """
        shortcut = self.get_shortcut(key, context)
        if shortcut:
            shortcut.enabled = False

    def clear(self) -> None:
        """Clear all registered shortcuts."""
        self._shortcuts.clear()

    def list_shortcuts(self, context: Optional[str] = None) -> str:
        """
        Get a formatted list of shortcuts.

        Args:
            context: Optional context to filter by

        Returns:
            Formatted string of shortcuts
        """
        shortcuts = self._shortcuts if context is None else self.get_shortcuts_by_context(context)

        if not shortcuts:
            return "No shortcuts registered."

        lines = []
        for shortcut in shortcuts:
            status = "✓" if shortcut.enabled else "✗"
            lines.append(f"{status} {shortcut.key:20} - {shortcut.description}")

        return "\n".join(lines)

    def get_help_text(self, context: Optional[str] = None) -> str:
        """
        Generate help text for shortcuts.

        Args:
            context: Optional context to filter by

        Returns:
            Help text string
        """
        shortcuts = self.get_enabled_shortcuts(context)

        if not shortcuts:
            return "No shortcuts available."

        lines = ["Keyboard Shortcuts:", ""]

        # Group by context
        contexts = {}
        for shortcut in shortcuts:
            if shortcut.context not in contexts:
                contexts[shortcut.context] = []
            contexts[shortcut.context].append(shortcut)

        for ctx, ctx_shortcuts in sorted(contexts.items()):
            lines.append(f"[{ctx.upper()}]")
            for shortcut in sorted(ctx_shortcuts, key=lambda s: s.key):
                lines.append(f"  {shortcut.key:20} - {shortcut.description}")
            lines.append("")

        return "\n".join(lines)

    def search(self, query: str) -> list[Shortcut]:
        """
        Search shortcuts by description or action.

        Args:
            query: Search query (case-insensitive)

        Returns:
            List of matching shortcuts
        """
        query_lower = query.lower()
        results = []

        for shortcut in self._shortcuts:
            if (
                query_lower in shortcut.description.lower()
                or query_lower in shortcut.action.lower()
            ):
                results.append(shortcut)

        return results

    def export_to_dict(self) -> dict:
        """
        Export shortcuts to dictionary format.

        Returns:
            Dictionary containing all shortcuts
        """
        return {"shortcuts": [s.to_dict() for s in self._shortcuts]}

    def import_from_dict(self, data: dict) -> None:
        """
        Import shortcuts from dictionary format.

        Args:
            data: Dictionary containing shortcuts
        """
        if "shortcuts" not in data:
            return

        for shortcut_data in data["shortcuts"]:
            shortcut = Shortcut.from_dict(shortcut_data)
            self._shortcuts.append(shortcut)

    def _remove_by_key_and_context(self, key: str, context: str) -> None:
        """
        Remove a shortcut by key and context.

        Args:
            key: The keyboard shortcut
            context: The context
        """
        self._shortcuts = [
            s for s in self._shortcuts if not (s.key == key and s.context == context)
        ]
