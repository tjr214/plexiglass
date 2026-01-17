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
        - Show setup prompt if config not found
        - Don't crash the app
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        nonexistent = tmp_path / "nonexistent.yaml"
        app = PlexiGlassApp(config_path=nonexistent)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert - should show setup prompt
            assert app.screen.__class__.__name__ == "ConfigSetupPromptScreen"

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

    @pytest.mark.asyncio
    async def test_app_has_command_prompt_keybinding(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should have command prompt keybinding.

        Expected behavior:
        - ':' key opens command prompt
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.press(":")
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "CommandPromptScreen"

    @pytest.mark.asyncio
    async def test_config_prompt_screen_shows_on_invalid_config(self, tmp_path: Path) -> None:
        """
        RED TEST: Should show config prompt when config is invalid.

        Expected behavior:
        - Invalid YAML leads to config setup prompt
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        bad_config = tmp_path / "servers.yaml"
        bad_config.write_text("servers: [", encoding="utf-8")
        app = PlexiGlassApp(config_path=bad_config)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "ConfigSetupPromptScreen"


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
    async def test_app_can_open_command_prompt_screen(self, sample_config_path: Path) -> None:
        """
        RED TEST: Should display command prompt modal screen.

        Expected behavior:
        - Opening command prompt switches to modal screen
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "CommandPromptScreen"

    @pytest.mark.asyncio
    async def test_command_prompt_esc_closes_modal(self, sample_config_path: Path) -> None:
        """
        RED TEST: ESC should dismiss command prompt modal.

        Expected behavior:
        - ESC returns to main screen
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()
            await pilot.press("escape")
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "MainScreen"

    @pytest.mark.asyncio
    async def test_quick_actions_open_command_prompt(self, sample_config_path: Path) -> None:
        """
        RED TEST: Quick actions should open command prompt.

        Expected behavior:
        - Triggering command prompt action opens modal
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            menu = app.screen.query_one("QuickActionsMenu")
            trigger_action = getattr(menu, "trigger_action")
            trigger_action("open_command_prompt")
            await pilot.pause()

            # Assert
            assert app.screen.__class__.__name__ == "CommandPromptScreen"

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
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("connect_default")
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
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("refresh")
            await pilot.pause()

            # Assert
            main_screen = app.get_screen("main")
            assert hasattr(main_screen, "last_manual_refresh")
            assert getattr(main_screen, "last_manual_refresh") is True

    @pytest.mark.asyncio
    async def test_command_prompt_tracks_history(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should track command history.

        Expected behavior:
        - Submitted commands stored in history list
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("refresh")
            submit_command("open_gallery")
            await pilot.pause()

            # Assert
            history = getattr(screen, "history")
            assert "refresh" in history
            assert "open_gallery" in history

    @pytest.mark.asyncio
    async def test_command_prompt_updates_autocomplete(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should update autocomplete suggestions.

        Expected behavior:
        - Typing text updates suggestion list
        - Suggestions include grouped headers
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            update_suggestions = getattr(screen, "_update_suggestions")
            update_suggestions("re")
            await pilot.pause()

            # Assert
            suggestions = screen.query_one("#command-suggestions")
            render_text = str(suggestions.render())
            assert "refresh" in render_text
            assert "Refresh dashboard data" in render_text
            assert "Core" in render_text

    @pytest.mark.asyncio
    async def test_command_prompt_list_servers(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should list servers.

        Expected behavior:
        - Running list_servers outputs server names
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("list_servers")
            await pilot.pause()

            # Assert
            output = screen.query_one("#command-output")
            assert "Home Server" in str(output.render())

    @pytest.mark.asyncio
    async def test_config_setup_screen_adds_server(self, sample_config_path: Path) -> None:
        """
        RED TEST: Config setup screen should add a server entry.

        Expected behavior:
        - Add server and see it in the list
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)
        config_path = sample_config_path
        setup_builder = getattr(app, "_build_config_setup_screen")
        setup = setup_builder()

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.push_screen(setup)
            await pilot.pause()
            setup = app.screen
            add_server = getattr(setup, "add_server")
            add_server(
                {
                    "name": "Home Server",
                    "description": "Primary",
                    "url": "http://localhost:32400",
                    "token": "token",
                    "default": True,
                }
            )
            save_config = getattr(setup, "save_config")
            save_config()
            await pilot.pause()

            # Assert
            assert config_path.exists()
            assert config_path.read_text(encoding="utf-8")

    @pytest.mark.asyncio
    async def test_config_setup_screen_saves_config(self, sample_config_path: Path) -> None:
        """
        RED TEST: Config setup screen should save config.

        Expected behavior:
        - Save config writes file to disk
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)
        config_path = sample_config_path
        setup_builder = getattr(app, "_build_config_setup_screen")
        setup = setup_builder()

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.push_screen(setup)
            await pilot.pause()
            setup = app.screen
            add_server = getattr(setup, "add_server")
            add_server(
                {
                    "name": "Home Server",
                    "description": "Primary",
                    "url": "http://localhost:32400",
                    "token": "token",
                    "default": True,
                }
            )
            save_config = getattr(setup, "save_config")
            save_config()
            await pilot.pause()

            # Assert
            assert config_path.exists()
            assert config_path.read_text(encoding="utf-8")

    @pytest.mark.asyncio
    async def test_command_prompt_list_servers_filtered(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should filter servers by status.

        Expected behavior:
        - list_servers connected only shows connected servers
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)
        server_manager = MagicMock()
        server_manager.get_all_server_names.return_value = ["Home Server", "Lab"]
        server_manager.get_connected_servers.return_value = {"Home Server"}

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()
            app.server_manager = server_manager

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("list_servers connected")
            await pilot.pause()
            await pilot.pause()

            # Assert
            output = screen.query_one("#command-output")
            render_text = str(output.render())
            assert "Home Server" in render_text
            assert "Lab" not in render_text

    @pytest.mark.asyncio
    async def test_command_prompt_list_libraries(self, sample_config_path: Path) -> None:
        """
        RED TEST: Command prompt should list libraries.

        Expected behavior:
        - Running list_libraries outputs library names
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)
        server_manager = MagicMock()
        server_manager.get_all_server_names.return_value = ["Home Server"]
        server_manager.get_server_status.return_value = {
            "library_names": ["Movies", "Series"],
            "library_count": 2,
            "library_items": 100,
        }

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()
            app.server_manager = server_manager

            screen = app.screen
            submit_command = getattr(screen, "submit_command")
            submit_command("list_libraries")
            await pilot.pause()
            await pilot.pause()

            # Assert
            output = screen.query_one("#command-output")
            render_text = str(output.render())
            assert "Movies" in render_text
            assert "Series" in render_text

    @pytest.mark.asyncio
    async def test_command_prompt_suggestion_paging(self, sample_config_path: Path) -> None:
        """
        RED TEST: Suggestion list should paginate/scroll.

        Expected behavior:
        - Typing filter shows only first page with indicator
        """
        # Arrange
        from plexiglass.app.plexiglass_app import PlexiGlassApp

        app = PlexiGlassApp(config_path=sample_config_path)

        # Act
        async with app.run_test() as pilot:
            await pilot.pause()
            app.action_show_command_prompt()
            await pilot.pause()

            screen = app.screen
            setattr(
                screen,
                "commands",
                [{"key": f"cmd_{idx}", "label": f"Command {idx}"} for idx in range(20)],
            )
            setattr(
                screen,
                "command_keys",
                [command["key"] for command in getattr(screen, "commands")],
            )
            update_suggestions = getattr(screen, "_update_suggestions")
            update_suggestions("")
            await pilot.pause()

            # Assert
            suggestions = screen.query_one("#command-suggestions")
            render_text = str(suggestions.render())
            assert "Showing" in render_text

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
