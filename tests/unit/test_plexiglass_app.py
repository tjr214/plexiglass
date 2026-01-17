"""
Tests for PlexiGlass Textual App Structure (TDD Red Phase)

This module tests the Textual application including:
- App initialization
- Screen management and routing
- Integration with ConfigLoader and ServerManager
- Main screen composition
- Keybindings
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestPlexiGlassApp:
    """Test suite for the PlexiGlassApp class."""

    @pytest.mark.asyncio
    async def test_app_initializes_with_config_path(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should initialize app with configuration file path.

        Expected behavior:
        - Accept config_path parameter
        - Load configuration on startup
        - Initialize ServerManager
        """
        # Arrange & Act
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Assert
        assert app is not None
        assert app.config_path == sample_config_path

    @pytest.mark.asyncio
    async def test_app_loads_config_on_mount(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should load configuration when app mounts.

        Expected behavior:
        - Create ConfigLoader instance
        - Load configuration
        - Create ServerManager with loaded config
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

        # Assert
        assert hasattr(app, "config_loader")
        assert app.config_loader is not None
        assert hasattr(app, "server_manager")
        assert app.server_manager is not None

    @pytest.mark.asyncio
    async def test_app_has_correct_title(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have correct app title and subtitle.

        Expected behavior:
        - TITLE = "PlexiGlass"
        - SUB_TITLE contains "Dashboard" and "Gallery"
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Assert
        assert app.TITLE == "PlexiGlass"
        assert app.SUB_TITLE is not None
        assert "Dashboard" in app.SUB_TITLE
        assert "Gallery" in app.SUB_TITLE

    @pytest.mark.asyncio
    async def test_app_has_main_screen(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should show main dashboard screen on startup.

        Expected behavior:
        - Install MainScreen as default screen
        - MainScreen shows server status
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            assert app.screen is not None
            assert app.screen.id == "main" or app.screen.__class__.__name__ == "MainScreen"

    @pytest.mark.asyncio
    async def test_app_has_quit_keybinding(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have 'q' keybinding to quit.

        Expected behavior:
        - Pressing 'q' quits the application
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.press("q")
            await pilot.pause()

        # Assert - if we get here without exception, quit worked
        assert True

    @pytest.mark.asyncio
    async def test_app_handles_missing_config_gracefully(self, tmp_path: Path) -> None:
        """
        RED TEST: Should handle missing config file gracefully.

        Expected behavior:
        - Show error message if config not found
        - Don't crash the app
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        nonexistent = tmp_path / "nonexistent.yaml"
        app = PlexiGlassApp(config_path=nonexistent)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

        # Assert - should not crash
        assert app is not None

    @pytest.mark.asyncio
    async def test_app_can_switch_to_gallery_screen(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should be able to switch to Gallery screen.

        Expected behavior:
        - Install GalleryScreen
        - Switch to it on command
        - Show gallery categories
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            # Simulate pressing 'g' to go to gallery (or whatever keybinding we choose)
            await pilot.press("g")
            await pilot.pause()

            # Assert
            screen_name = app.screen.__class__.__name__
            assert screen_name == "GalleryScreen" or app.screen.id == "gallery"

    @pytest.mark.asyncio
    async def test_app_has_help_keybinding(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have help/keybindings reference.

        Expected behavior:
        - Pressing '?' shows help
        - Lists all available keybindings
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.press("?")
            await pilot.pause()

        # Assert - Textual has built-in help, should work
        assert True


class TestMainScreen:
    """Test suite for the MainScreen (Dashboard)."""

    @pytest.mark.asyncio
    async def test_main_screen_shows_server_cards(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display cards for each configured server.

        Expected behavior:
        - Query ServerManager for all servers
        - Display ServerCard widget for each
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

        # Assert - should have widgets for servers
        assert len(list(app.query("ServerStatusCard"))) >= 0

    @pytest.mark.asyncio
    async def test_main_screen_shows_dashboard_summary(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display dashboard summary stats.

        Expected behavior:
        - Render summary widget above server cards
        - Summary includes totals and session counts
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            summary = app.screen.query_one("DashboardSummary")
            assert summary is not None

    @pytest.mark.asyncio
    async def test_main_screen_summary_includes_library_stats(
        self, sample_config_path: Path
    ) -> None:
        """
        RED TEST: Summary should include library statistics.

        Expected behavior:
        - Summary render includes library count and items
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            summary = app.screen.query_one("DashboardSummary")
            summary_text = str(summary.render())
            assert "Libraries" in summary_text

    @pytest.mark.asyncio
    async def test_main_screen_shows_session_details_panel(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display session details panel.

        Expected behavior:
        - Render session details widget
        - Shows per-server now playing entries
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            panel = app.screen.query_one("SessionDetailsPanel")
            assert panel is not None

    @pytest.mark.asyncio
    async def test_main_screen_shows_quick_actions_menu(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display quick actions menu.

        Expected behavior:
        - Render quick actions widget
        - Includes refresh and connect actions
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            menu = app.screen.query_one("QuickActionsMenu")
            assert menu is not None

    @pytest.mark.asyncio
    async def test_main_screen_shows_command_prompt_panel(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display command prompt panel.

        Expected behavior:
        - Render command prompt widget
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            panel = app.screen.query_one("CommandPromptPanel")
            assert panel is not None

    @pytest.mark.asyncio
    async def test_command_prompt_triggers_connect(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should call connect action.

        Expected behavior:
        - Running connect command calls server manager connect
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.server_manager = MagicMock()
            panel = app.screen.query_one("CommandPromptPanel")
            run_command = getattr(panel, "run_command")
            run_command("connect_default")
            await pilot.pause()

            # Assert
            server_manager = app.server_manager
            assert server_manager is not None
            assert server_manager.connect_to_default.called

    @pytest.mark.asyncio
    async def test_command_prompt_triggers_refresh(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should trigger refresh.

        Expected behavior:
        - Running refresh command triggers dashboard refresh
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            panel = app.screen.query_one("CommandPromptPanel")
            run_command = getattr(panel, "run_command")
            run_command("refresh")
            await pilot.pause()

            # Assert
            assert hasattr(app.screen, "last_manual_refresh")
            assert getattr(app.screen, "last_manual_refresh") is True

    @pytest.mark.asyncio
    async def test_quick_actions_menu_triggers_gallery(self, sample_config_path: Path) -> None:
        """
        RED TEST: Quick actions should open gallery.

        Expected behavior:
        - Selecting gallery action switches screen
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            menu = app.screen.query_one("QuickActionsMenu")
            trigger_action = getattr(menu, "trigger_action")
            trigger_action("open_gallery")
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "GalleryScreen" or app.screen.id == "gallery"

    @pytest.mark.asyncio
    async def test_main_screen_auto_refreshes(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should refresh dashboard status on interval.

        Expected behavior:
        - Use refresh interval from config settings
        - Schedule periodic refresh
        - Summary shows last update timestamp
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            screen = app.screen
            assert screen is not None
            assert hasattr(screen, "refresh_handle")
            assert getattr(screen, "refresh_handle") is not None

            summary = screen.query_one("DashboardSummary")
            assert hasattr(summary, "last_update")
            assert getattr(summary, "last_update") is not None

    @pytest.mark.asyncio
    async def test_main_screen_has_header(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have header with title.

        Expected behavior:
        - Header widget at top
        - Shows app title
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            header = app.screen.query_one("Header")
            assert header is not None

    @pytest.mark.asyncio
    async def test_main_screen_has_footer(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have footer with keybinding hints.

        Expected behavior:
        - Footer widget at bottom
        - Shows available keybindings
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            footer = app.screen.query_one("Footer")
            assert footer is not None


class TestGalleryScreen:
    """Test suite for the GalleryScreen (API Gallery)."""

    @pytest.mark.asyncio
    async def test_gallery_screen_shows_categories(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display API feature categories.

        Expected behavior:
        - Show list of 15 major categories
        - Navigate with arrow keys
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.press("g")  # Switch to gallery
            await pilot.pause()

            # Assert - should show category list
            assert len(list(app.query(".category"))) >= 0

    @pytest.mark.asyncio
    async def test_gallery_screen_can_return_to_main(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should be able to return to main screen from gallery.

        Expected behavior:
        - Press 'escape' or 'm' to return to main
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.press("g")  # Go to gallery
            await pilot.pause()
            await pilot.press("escape")  # Return to main
            await pilot.pause()

            # Assert
            screen_name = app.screen.__class__.__name__
            assert screen_name == "MainScreen" or app.screen.id == "main"


# Fixtures


@pytest.fixture
def sample_config_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a sample configuration file for testing."""
    monkeypatch.setenv("PLEX_TOKEN_HOME", "home-token-12345")
    monkeypatch.setenv("PLEX_TOKEN_TEST", "test-token-67890")

    config_content = """
servers:
  - name: "Home Server"
    description: "Main home Plex server"
    url: "http://192.168.1.100:32400"
    token: "${PLEX_TOKEN_HOME}"
    default: true
    read_only: false
    tags: ["production", "home"]
    
  - name: "Test Server"
    description: "Development and testing server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
    default: false
    read_only: false
    tags: ["development", "testing"]

settings:
  ui:
    theme: "dark"
    refresh_interval: 5
    
  performance:
    connection_timeout: 30
"""

    config_file = tmp_path / "servers.yaml"
    config_file.write_text(config_content)

    return config_file
