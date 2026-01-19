"""
Unit tests for KeyboardShortcutManager service.

Tests the keyboard shortcut management system including:
- Registration and unregistration
- Conflict detection
- Context-aware shortcuts
- Customization
- Help text generation
"""

import pytest
from plexiglass.services.keyboard_manager import (
    KeyboardShortcutManager,
    Shortcut,
    ShortcutConflict,
)


class TestShortcut:
    """Test the Shortcut model."""

    def test_shortcut_creation(self):
        """Test creating a shortcut."""
        shortcut = Shortcut(
            key="ctrl+s", action="save", description="Save the current file", context="global"
        )
        assert shortcut.key == "ctrl+s"
        assert shortcut.action == "save"
        assert shortcut.description == "Save the current file"
        assert shortcut.context == "global"

    def test_shortcut_equality(self):
        """Test shortcut equality comparison."""
        shortcut1 = Shortcut(key="ctrl+s", action="save", description="Save")
        shortcut2 = Shortcut(key="ctrl+s", action="save", description="Save")
        shortcut3 = Shortcut(key="ctrl+o", action="open", description="Open")

        assert shortcut1 == shortcut2
        assert shortcut1 != shortcut3

    def test_shortcut_repr(self):
        """Test shortcut string representation."""
        shortcut = Shortcut(key="ctrl+s", action="save", description="Save")
        assert "ctrl+s" in repr(shortcut)
        assert "save" in repr(shortcut)


class TestKeyboardShortcutManager:
    """Test the KeyboardShortcutManager service."""

    def test_manager_initialization(self):
        """Test manager initializes with empty registry."""
        manager = KeyboardShortcutManager()
        assert manager.get_all_shortcuts() == []

    def test_register_shortcut(self):
        """Test registering a new shortcut."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save file")

        shortcuts = manager.get_all_shortcuts()
        assert len(shortcuts) == 1
        assert shortcuts[0].key == "ctrl+s"
        assert shortcuts[0].action == "save"

    def test_register_duplicate_key_raises_conflict(self):
        """Test that registering duplicate key raises conflict."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")

        with pytest.raises(ShortcutConflict) as exc_info:
            manager.register(key="ctrl+s", action="other", description="Other")

        assert "ctrl+s" in str(exc_info.value)

    def test_unregister_shortcut(self):
        """Test unregistering a shortcut."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")
        assert len(manager.get_all_shortcuts()) == 1

        manager.unregister("ctrl+s")
        assert len(manager.get_all_shortcuts()) == 0

    def test_unregister_nonexistent_shortcut(self):
        """Test unregistering a non-existent shortcut."""
        manager = KeyboardShortcutManager()

        # Should not raise error
        manager.unregister("ctrl+x")
        assert len(manager.get_all_shortcuts()) == 0

    def test_get_shortcut_by_key(self):
        """Test getting a specific shortcut by key."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")

        shortcut = manager.get_shortcut("ctrl+s")
        assert shortcut is not None
        assert shortcut.key == "ctrl+s"

    def test_get_nonexistent_shortcut(self):
        """Test getting a non-existent shortcut returns None."""
        manager = KeyboardShortcutManager()

        shortcut = manager.get_shortcut("ctrl+x")
        assert shortcut is None

    def test_context_aware_shortcuts(self):
        """Test shortcuts with different contexts."""
        manager = KeyboardShortcutManager()

        # Same key, different contexts should be allowed
        manager.register(
            key="ctrl+s", action="save_dashboard", description="Save dashboard", context="dashboard"
        )
        manager.register(
            key="ctrl+s", action="save_gallery", description="Save gallery", context="gallery"
        )

        # Both should be registered
        shortcuts = manager.get_all_shortcuts()
        assert len(shortcuts) == 2

    def test_get_shortcuts_by_context(self):
        """Test getting shortcuts for a specific context."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save", context="dashboard")
        manager.register(key="ctrl+o", action="open", description="Open", context="dashboard")
        manager.register(key="ctrl+g", action="gallery", description="Gallery", context="global")

        dashboard_shortcuts = manager.get_shortcuts_by_context("dashboard")
        assert len(dashboard_shortcuts) == 2

        global_shortcuts = manager.get_shortcuts_by_context("global")
        assert len(global_shortcuts) == 1

    def test_check_conflict_detection(self):
        """Test conflict detection without raising."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")

        # Should detect conflict
        has_conflict = manager.has_conflict("ctrl+s", context="global")
        assert has_conflict is True

        # Should not detect conflict for different key
        has_conflict = manager.has_conflict("ctrl+o", context="global")
        assert has_conflict is False

    def test_override_shortcut(self):
        """Test overriding an existing shortcut."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")

        # Override with force=True
        manager.register(key="ctrl+s", action="save_new", description="Save New", force=True)

        shortcut = manager.get_shortcut("ctrl+s")
        assert shortcut.action == "save_new"

    def test_list_all_shortcuts_formatted(self):
        """Test getting formatted list of all shortcuts."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save file")
        manager.register(key="ctrl+o", action="open", description="Open file")

        formatted = manager.list_shortcuts()
        assert "ctrl+s" in formatted
        assert "Save file" in formatted
        assert "ctrl+o" in formatted
        assert "Open file" in formatted

    def test_clear_all_shortcuts(self):
        """Test clearing all registered shortcuts."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")
        manager.register(key="ctrl+o", action="open", description="Open")

        assert len(manager.get_all_shortcuts()) == 2

        manager.clear()
        assert len(manager.get_all_shortcuts()) == 0

    def test_enable_disable_shortcut(self):
        """Test enabling/disabling individual shortcuts."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")

        shortcut = manager.get_shortcut("ctrl+s")
        assert shortcut.enabled is True

        manager.disable("ctrl+s")
        shortcut = manager.get_shortcut("ctrl+s")
        assert shortcut.enabled is False

        manager.enable("ctrl+s")
        shortcut = manager.get_shortcut("ctrl+s")
        assert shortcut.enabled is True

    def test_get_enabled_shortcuts_only(self):
        """Test getting only enabled shortcuts."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")
        manager.register(key="ctrl+o", action="open", description="Open")

        manager.disable("ctrl+o")

        enabled = manager.get_enabled_shortcuts()
        assert len(enabled) == 1
        assert enabled[0].key == "ctrl+s"

    def test_get_help_text(self):
        """Test generating help text for shortcuts."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save file")
        manager.register(key="ctrl+q", action="quit", description="Quit app")

        help_text = manager.get_help_text()
        assert "ctrl+s" in help_text
        assert "Save file" in help_text
        assert "ctrl+q" in help_text
        assert "Quit app" in help_text

    def test_search_shortcuts(self):
        """Test searching shortcuts by description or action."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save the current file")
        manager.register(key="ctrl+o", action="open", description="Open a file")
        manager.register(key="ctrl+q", action="quit", description="Quit application")

        # Search by description
        results = manager.search("file")
        assert len(results) == 2

        # Search by action
        results = manager.search("quit")
        assert len(results) == 1
        assert results[0].key == "ctrl+q"

    def test_export_shortcuts_to_dict(self):
        """Test exporting shortcuts to dictionary format."""
        manager = KeyboardShortcutManager()

        manager.register(key="ctrl+s", action="save", description="Save")
        manager.register(key="ctrl+o", action="open", description="Open")

        exported = manager.export_to_dict()
        assert "shortcuts" in exported
        assert len(exported["shortcuts"]) == 2
        assert exported["shortcuts"][0]["key"] == "ctrl+s"

    def test_import_shortcuts_from_dict(self):
        """Test importing shortcuts from dictionary format."""
        manager = KeyboardShortcutManager()

        data = {
            "shortcuts": [
                {"key": "ctrl+s", "action": "save", "description": "Save", "context": "global"},
                {"key": "ctrl+o", "action": "open", "description": "Open", "context": "global"},
            ]
        }

        manager.import_from_dict(data)

        shortcuts = manager.get_all_shortcuts()
        assert len(shortcuts) == 2
