"""
PlexiGlass - Main Textual Application.

Provides the foundation for the PlexiGlass TUI including:
- Configuration loading
- Server management initialization
- Screen routing (Main + Gallery)
- Basic layout scaffolding
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Static


from plexiglass.config.loader import ConfigLoader
from plexiglass.services.server_manager import ServerManager


class ServerCard(Static):
    """Minimal server card widget for the dashboard."""

    def __init__(self, server_name: str, **kwargs: Any) -> None:
        super().__init__(server_name, **kwargs)
        self.server_name = server_name


class MainScreen(Screen):
    """Main dashboard screen showing server status cards."""

    def compose(self) -> ComposeResult:
        yield Header()

        server_names: list[str] = []
        app = self.app
        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            server_names = app.server_manager.get_all_server_names()

        for name in server_names:
            yield ServerCard(name)

        yield Footer()


class GalleryScreen(Screen):
    """Gallery screen for python-plexapi feature categories."""

    CATEGORY_NAMES = [
        "Server & Connection",
        "Library Management",
        "Media Operations",
        "Playback & Clients",
        "Collections & Playlists",
        "Users & Sharing",
        "MyPlex Account",
        "Settings & Preferences",
        "Search & Discovery",
        "Sync & Offline",
        "Alerts & Monitoring",
        "Integrations",
        "Media Analysis",
        "Utilities",
        "Advanced Features",
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        for category in self.CATEGORY_NAMES:
            yield Static(category, classes="category")

        yield Footer()


class PlexiGlassApp(App):
    """
    PlexiGlass - Multi-server Plex dashboard and python-plexapi feature gallery.

    This is the main Textual application class.
    """

    TITLE = "PlexiGlass"
    SUB_TITLE = "Plex Media Server Dashboard & API Gallery"

    SCREENS = {
        "main": MainScreen,
        "gallery": GalleryScreen,
    }
    DEFAULT_SCREEN = "main"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("g", "show_gallery", "Gallery"),
        ("m", "show_main", "Main"),
        ("escape", "show_main", "Main"),
        ("?", "help", "Help"),
    ]

    def __init__(self, config_path: Path | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.config_path = config_path or Path("config/servers.yaml")
        self.config_loader: ConfigLoader | None = None
        self.server_manager: ServerManager | None = None
        self.error_message: str | None = None

    def on_mount(self) -> None:
        """Initialize services and screens when app mounts."""
        self._load_configuration()
        self.push_screen("main")

    def _load_configuration(self) -> None:
        """Load configuration and initialize the server manager."""
        try:
            loader = ConfigLoader(self.config_path)
            loader.load()
            self.config_loader = loader
            self.server_manager = ServerManager(loader)
        except Exception as exc:  # noqa: BLE001 - surface error to UI later
            self.error_message = str(exc)
            self.config_loader = None
            self.server_manager = None

    def action_show_gallery(self) -> None:
        """Switch to the Gallery screen."""
        self.switch_screen("gallery")

    def action_show_main(self) -> None:
        """Switch to the Main screen."""
        self.switch_screen("main")

    def action_help(self) -> None:
        """Placeholder help action (Textual will handle help overlay)."""
        return None
