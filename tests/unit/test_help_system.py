"""
Tests for Help System (HelpScreen and HelpContent).
"""

import pytest
from textual.app import App
from plexiglass.ui.screens.help_screen import HelpScreen
from plexiglass.services.help_content import HelpContent


class TestHelpContent:
    """Test suite for HelpContent service."""

    def test_help_content_initialization(self):
        """Test HelpContent can be instantiated."""
        help_content = HelpContent()
        assert help_content is not None

    def test_get_all_topics(self):
        """Test getting all help topics."""
        help_content = HelpContent()
        topics = help_content.get_all_topics()

        assert len(topics) > 0
        assert "Dashboard Mode" in [t["title"] for t in topics]
        assert "Gallery Mode" in [t["title"] for t in topics]
        assert "Keyboard Shortcuts" in [t["title"] for t in topics]

    def test_get_topic_by_id(self):
        """Test getting specific topic by ID."""
        help_content = HelpContent()
        topic = help_content.get_topic("dashboard")

        assert topic is not None
        assert topic["id"] == "dashboard"
        assert "title" in topic
        assert "content" in topic

    def test_get_nonexistent_topic(self):
        """Test getting non-existent topic returns None."""
        help_content = HelpContent()
        topic = help_content.get_topic("nonexistent")

        assert topic is None

    def test_search_help_content(self):
        """Test searching help content."""
        help_content = HelpContent()
        results = help_content.search("gallery")

        assert len(results) > 0
        assert any("gallery" in r["title"].lower() for r in results)

    def test_search_case_insensitive(self):
        """Test search is case-insensitive."""
        help_content = HelpContent()
        results_lower = help_content.search("dashboard")
        results_upper = help_content.search("DASHBOARD")

        assert len(results_lower) == len(results_upper)

    def test_search_empty_query(self):
        """Test search with empty query returns all topics."""
        help_content = HelpContent()
        results = help_content.search("")
        all_topics = help_content.get_all_topics()

        assert len(results) == len(all_topics)

    def test_get_keyboard_shortcuts(self):
        """Test getting keyboard shortcuts reference."""
        help_content = HelpContent()
        shortcuts = help_content.get_keyboard_shortcuts()

        assert len(shortcuts) > 0
        assert any(s["key"] == "d" for s in shortcuts)  # Dashboard
        assert any(s["key"] == "g" for s in shortcuts)  # Gallery
        assert any(s["key"] == "h" or s["key"] == "F1" for s in shortcuts)  # Help

    def test_get_shortcuts_by_category(self):
        """Test getting shortcuts grouped by category."""
        help_content = HelpContent()
        shortcuts = help_content.get_keyboard_shortcuts()

        # Should have categories
        categories = set(s.get("category", "General") for s in shortcuts)
        assert len(categories) > 1

    def test_get_context_help(self):
        """Test getting context-sensitive help."""
        help_content = HelpContent()

        # Dashboard context
        dashboard_help = help_content.get_context_help("dashboard")
        assert dashboard_help is not None
        assert "dashboard" in dashboard_help["content"].lower()

        # Gallery context
        gallery_help = help_content.get_context_help("gallery")
        assert gallery_help is not None
        assert "gallery" in gallery_help["content"].lower()


class TestHelpScreen:
    """Test suite for HelpScreen."""

    @pytest.mark.asyncio
    async def test_help_screen_creation(self):
        """Test HelpScreen can be created."""
        screen = HelpScreen()
        assert screen is not None

    @pytest.mark.asyncio
    async def test_help_screen_has_search(self):
        """Test HelpScreen has search functionality."""
        screen = HelpScreen()
        assert hasattr(screen, "search_query")

    @pytest.mark.asyncio
    async def test_help_screen_has_topic_list(self):
        """Test HelpScreen displays topic list."""
        screen = HelpScreen()
        assert hasattr(screen, "topic_list")

    @pytest.mark.asyncio
    async def test_help_screen_has_content_display(self):
        """Test HelpScreen has content display area."""
        screen = HelpScreen()
        assert hasattr(screen, "content_display")

    @pytest.mark.asyncio
    async def test_help_screen_initial_topic(self):
        """Test HelpScreen can be initialized with specific topic."""
        screen = HelpScreen(initial_topic="dashboard")
        assert screen.initial_topic == "dashboard"

    @pytest.mark.asyncio
    async def test_help_screen_default_topic(self):
        """Test HelpScreen defaults to overview topic."""
        screen = HelpScreen()
        assert screen.initial_topic == "overview" or screen.initial_topic is None

    @pytest.mark.asyncio
    async def test_help_screen_select_topic(self):
        """Test selecting a topic in HelpScreen."""
        screen = HelpScreen()
        screen.select_topic("gallery")
        assert screen.current_topic == "gallery"

    @pytest.mark.asyncio
    async def test_help_screen_search_topics(self):
        """Test searching topics in HelpScreen."""
        screen = HelpScreen()
        screen.search_topics("keyboard")
        assert screen.search_query == "keyboard"

    @pytest.mark.asyncio
    async def test_help_screen_clear_search(self):
        """Test clearing search in HelpScreen."""
        screen = HelpScreen()
        screen.search_topics("test")
        assert screen.search_query == "test"

        screen.clear_search()
        assert screen.search_query == ""

    @pytest.mark.asyncio
    async def test_help_screen_dismissible(self):
        """Test HelpScreen can be dismissed with ESC."""
        screen = HelpScreen()
        # Should have ESC binding
        bindings = [b[0] for b in screen.BINDINGS]
        assert "escape" in bindings or "q" in bindings
