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
from textual.message import Message
from textual.widgets import Footer, Header, Static

from plexiglass.config.loader import ConfigLoader
from plexiglass.services.server_manager import ServerManager


class DashboardSummary(Static):
    """Dashboard summary widget for aggregate stats."""

    def __init__(self, summary: dict[str, Any], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.summary = summary

    def on_mount(self) -> None:
        self.update(self._render_summary())

    def update_summary(self, summary: dict[str, Any]) -> None:
        self.summary = summary
        self.update(self._render_summary())

    def _render_summary(self) -> str:
        total = self.summary.get("total_servers", 0)
        connected = self.summary.get("connected_servers", 0)
        sessions = self.summary.get("active_sessions", 0)
        return (
            "Dashboard Summary\n"
            f"Servers: {total} | Connected: {connected} | Active Sessions: {sessions}"
        )


class ServerStatusCard(Static):
    """Server status widget for the dashboard."""

    def __init__(self, status: dict[str, Any], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.status = status

    def on_mount(self) -> None:
        self.update(self._render_status())

    def update_status(self, status: dict[str, Any]) -> None:
        self.status = status
        self.update(self._render_status())

    def _render_status(self) -> str:
        name = self.status.get("name", "Unknown")
        url = self.status.get("url", "")
        connected = "Connected" if self.status.get("connected") else "Disconnected"
        version = self.status.get("version", "-")
        platform = self.status.get("platform", "-")
        session_count = self.status.get("session_count", 0)
        now_playing = self._format_now_playing(self.status.get("now_playing", []))

        lines = [
            f"{name}",
            f"{connected} | {url}",
            f"Version: {version} | Platform: {platform}",
            f"Sessions: {session_count}",
        ]

        if now_playing:
            lines.append("Now Playing:")
            lines.extend(now_playing)

        return "\n".join(lines)

    @staticmethod
    def _format_now_playing(entries: list[dict[str, Any]]) -> list[str]:
        formatted: list[str] = []
        for entry in entries:
            title = entry.get("title", "Unknown")
            user = entry.get("user", "Unknown")
            state = entry.get("state", "unknown")
            progress = entry.get("progress_percent")
            progress_display = "-" if progress is None else f"{progress}%"
            formatted.append(f"- {title} ({user}) [{state}] {progress_display}")

        return formatted


class MainScreen(Screen):
    """Main dashboard screen showing server status cards."""

    refresh_handle = None

    class DashboardRefresh(Message):
        """Message for refreshing dashboard data."""

    def compose(self) -> ComposeResult:
        yield Header()

        summary = self._build_summary()
        yield DashboardSummary(summary)

        server_names: list[str] = []
        app = self.app
        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            server_names = app.server_manager.get_all_server_names()

        for name in server_names:
            status = self._get_server_status(name)
            yield ServerStatusCard(status)

        yield Footer()

    def on_mount(self) -> None:
        app = self.app
        refresh_interval = 5
        if isinstance(app, PlexiGlassApp) and app.config_loader is not None:
            refresh_interval = (
                app.config_loader.get_settings().get("ui", {}).get("refresh_interval", 5)
            )
        self.refresh_handle = self.set_interval(refresh_interval, self._trigger_refresh)

    def _trigger_refresh(self) -> None:
        self.post_message(self.DashboardRefresh())

    def on_main_screen_dashboard_refresh(self, message: "MainScreen.DashboardRefresh") -> None:
        del message
        self._refresh_dashboard()

    def _refresh_dashboard(self) -> None:
        app = self.app
        summary_widget: DashboardSummary = self.query_one(DashboardSummary)
        summary_widget.update_summary(self._build_summary())

        for card in self.query(ServerStatusCard):
            status = self._get_server_status(card.status.get("name", ""))
            card.update_status(status)

    def _get_server_status(self, name: str) -> dict[str, Any]:
        app = self.app
        status: dict[str, Any] = {
            "name": name,
            "connected": False,
            "session_count": 0,
            "now_playing": [],
        }
        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            status = app.server_manager.get_server_status(name)
        return status

    def _build_summary(self) -> dict[str, Any]:
        app = self.app
        server_names: list[str] = []
        connected_count = 0
        session_count = 0

        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            server_names = app.server_manager.get_all_server_names()
            for name in server_names:
                status = app.server_manager.get_server_status(name)
                if status.get("connected"):
                    connected_count += 1
                session_count += int(status.get("session_count", 0))

        return {
            "total_servers": len(server_names),
            "connected_servers": connected_count,
            "active_sessions": session_count,
        }


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
