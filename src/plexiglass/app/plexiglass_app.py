"""
PlexiGlass - Main Textual Application.

Provides the foundation for the PlexiGlass TUI including:
- Configuration loading
- Server management initialization
- Screen routing (Main + Gallery)
- Basic layout scaffolding
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Static

from plexiglass.config.loader import ConfigLoader
from plexiglass.services.server_manager import ServerManager


class DashboardSummary(Static):
    """Dashboard summary widget for aggregate stats."""

    def __init__(self, summary: dict[str, Any], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.summary = summary
        self.last_update: str | None = None
        self.add_class("dashboard-summary")

    def on_mount(self) -> None:
        self.update(self._render_summary())

    def update_summary(self, summary: dict[str, Any], last_update: str | None = None) -> None:
        self.summary = summary
        if last_update is not None:
            self.last_update = last_update
        self.update(self._render_summary())

    def _render_summary(self) -> str:
        total = self.summary.get("total_servers", 0)
        connected = self.summary.get("connected_servers", 0)
        sessions = self.summary.get("active_sessions", 0)
        libraries = self.summary.get("total_libraries", 0)
        library_items = self.summary.get("total_library_items", 0)
        last_update = self.last_update or "-"
        return (
            "Dashboard Summary\n"
            f"Servers: {total} | Connected: {connected} | Active Sessions: {sessions}\n"
            f"Libraries: {libraries} | Items: {library_items}\n"
            f"[highlight]Last Update[/]: {last_update}"
        )


class SessionDetailsPanel(Static):
    """Detailed session list panel for all servers."""

    def __init__(self, sessions: list[dict[str, Any]], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.sessions = sessions
        self.add_class("session-panel")

    def on_mount(self) -> None:
        self.update(self._render_sessions())

    def update_sessions(self, sessions: list[dict[str, Any]]) -> None:
        self.sessions = sessions
        self.update(self._render_sessions())

    def _render_sessions(self) -> str:
        if not self.sessions:
            return "Active Sessions\nNone"

        lines = ["Active Sessions"]
        for entry in self.sessions:
            server = entry.get("server", "Unknown")
            title = entry.get("title", "Unknown")
            user = entry.get("user", "Unknown")
            state = entry.get("state", "unknown")
            progress = entry.get("progress_percent")
            progress_display = "-" if progress is None else f"{progress}%"
            lines.append(f"{server}: {title} ({user}) [{state}] {progress_display}")

        return "\n".join(lines)


class QuickActionsMenu(Static):
    """Quick actions menu for dashboard shortcuts."""

    def __init__(self, actions: list[str], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.actions = actions
        self.add_class("quick-actions")

    def on_mount(self) -> None:
        self.update(self._render_actions())

    def update_actions(self, actions: list[str]) -> None:
        self.actions = actions
        self.update(self._render_actions())

    def trigger_action(self, action_key: str) -> None:
        self.post_message(self.ActionTriggered(action_key))

    def _render_actions(self) -> str:
        if not self.actions:
            return "Quick Actions\nNone"
        return "Quick Actions\n" + "\n".join(f"- {action}" for action in self.actions)

    class ActionTriggered(Message):
        """Message fired when a quick action is triggered."""

        bubble = True

        def __init__(self, action_key: str) -> None:
            super().__init__()
            self.action_key = action_key


class CommandPromptPanel(Static):
    """Popup command prompt panel for dashboard actions."""

    def __init__(self, commands: list[str], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.commands = commands
        self.last_output: str | None = None
        self.add_class("command-prompt")

    def on_mount(self) -> None:
        self.update(self._render_prompt())

    def update_commands(self, commands: list[str]) -> None:
        self.commands = commands
        self.update(self._render_prompt())

    def set_output(self, output: str) -> None:
        self.last_output = output
        self.update(self._render_prompt())

    def run_command(self, command: str) -> None:
        self.post_message(self.CommandSubmitted(command.strip()))

    def _render_prompt(self) -> str:
        lines = ["Command Prompt"]
        if self.commands:
            lines.append("Commands:")
            lines.extend(f"- {command}" for command in self.commands)
        if self.last_output:
            lines.append("Output:")
            lines.append(self.last_output)
        return "\n".join(lines)

    class CommandSubmitted(Message):
        """Message fired when a command is submitted."""

        bubble = True

        def __init__(self, command: str) -> None:
            super().__init__()
            self.command = command


class CommandPromptScreen(Screen):
    """Modal command prompt screen."""

    def __init__(self, commands: list[str], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.commands = commands
        self.history: list[str] = []
        self.last_output: str | None = None

    def compose(self) -> ComposeResult:
        with Container(classes="command-modal"):
            yield Static("Command Prompt", classes="modal-title")
            if self.commands:
                yield Static("Commands:", classes="modal-section")
                for command in self.commands:
                    yield Static(f"- {command}")
            yield Static("History:", classes="modal-section")
            yield Static("", id="history")
            yield Static("Suggestions:", classes="modal-section")
            yield Static("", id="command-suggestions")
            yield Input(placeholder="Type a command and press enter", id="command-input")
            yield Static("", id="command-output")

    def on_mount(self) -> None:
        input_widget = self.query_one("#command-input", Input)
        input_widget.focus()
        self._update_suggestions("")

    def submit_command(self, command: str) -> None:
        normalized = command.strip()
        if not normalized:
            return
        self.history.append(normalized)
        if len(self.history) > 10:
            self.history = self.history[-10:]
        self.query_one("#history", Static).update("\n".join(self.history))
        self._update_suggestions("")
        self.post_message(self.CommandSubmitted(normalized))
        if isinstance(self.app, PlexiGlassApp):
            self.app.post_message(self.CommandSubmitted(normalized))
            self.app.call_later(self.app._handle_command_prompt_command, normalized)

    def set_output(self, output: str) -> None:
        self.last_output = output
        try:
            self.query_one("#command-output", Static).update(output)
        except Exception:
            return

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.submit_command(event.value)
        event.input.value = ""

    def on_input_changed(self, event: Input.Changed) -> None:
        self._update_suggestions(event.value)

    def _update_suggestions(self, text: str) -> None:
        normalized = text.strip().lower()
        matches = [command for command in self.commands if command.lower().startswith(normalized)]
        if not normalized:
            matches = self.commands
        suggestions = "\n".join(matches) if matches else "No suggestions"
        self.query_one("#command-suggestions", Static).update(suggestions)

    class CommandSubmitted(Message):
        """Message fired when a command is submitted."""

        bubble = True

        def __init__(self, command: str) -> None:
            super().__init__()
            self.command = command


class ServerStatusCard(Static):
    """Server status widget for the dashboard."""

    def __init__(self, status: dict[str, Any], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.status = status
        self.add_class("status-card")
        self._apply_status_class()

    def on_mount(self) -> None:
        self._apply_status_class()
        self.update(self._render_status())

    def update_status(self, status: dict[str, Any]) -> None:
        self.status = status
        self._apply_status_class()
        self.update(self._render_status())

    def _apply_status_class(self) -> None:
        if self.status.get("connected"):
            self.add_class("connected")
            self.remove_class("disconnected")
        else:
            self.add_class("disconnected")
            self.remove_class("connected")

    def _render_status(self) -> str:
        name = self.status.get("name", "Unknown")
        url = self.status.get("url", "")
        connected = "Connected" if self.status.get("connected") else "Disconnected"
        version = self.status.get("version", "-")
        platform = self.status.get("platform", "-")
        session_count = self.status.get("session_count", 0)
        now_playing = self._format_now_playing(self.status.get("now_playing", []))
        status_style = "[green]" if self.status.get("connected") else "[red]"

        lines = [
            f"{name}",
            f"{status_style}{connected}[/] | {url}",
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
    last_manual_refresh = False

    class DashboardRefresh(Message):
        """Message for refreshing dashboard data."""

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(id="dashboard", classes="dashboard"):
            summary = self._build_summary()
            yield DashboardSummary(summary)

            with Horizontal(classes="dashboard-row"):
                actions = self._build_quick_actions()
                yield QuickActionsMenu(actions)

                commands = self._build_command_prompt_commands()
                yield CommandPromptPanel(commands)

            yield Static("", classes="panel-spacer")

            sessions = self._build_session_details()
            yield SessionDetailsPanel(sessions)

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
        summary_widget: DashboardSummary = self.query_one(DashboardSummary)
        summary_widget.update_summary(
            self._build_summary(), last_update=self._format_timestamp(datetime.now())
        )

    def _trigger_refresh(self) -> None:
        self.post_message(self.DashboardRefresh())

    def on_main_screen_dashboard_refresh(self, message: "MainScreen.DashboardRefresh") -> None:
        del message
        self._refresh_dashboard()

    def on_quick_actions_menu_action_triggered(
        self, message: "QuickActionsMenu.ActionTriggered"
    ) -> None:
        self._handle_command(message.action_key)

    def on_command_prompt_panel_command_submitted(
        self, message: "CommandPromptPanel.CommandSubmitted"
    ) -> None:
        self._handle_command(message.command)

    def on_command_prompt_screen_command_submitted(
        self, message: "CommandPromptScreen.CommandSubmitted"
    ) -> None:
        self._handle_command(message.command)

    def _handle_command(self, command: str) -> None:
        normalized = command.strip().lower()
        main_screen = self.app.get_screen("main") if self.app is not None else None
        if normalized in {"refresh", "refresh dashboard"}:
            if isinstance(main_screen, MainScreen):
                main_screen.last_manual_refresh = True
                main_screen._refresh_dashboard()
            self._set_command_output("Dashboard refreshed")
            return
        if normalized in {"connect", "connect_default", "connect default"}:
            app = self.app
            if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
                app.server_manager.connect_to_default()
                self._set_command_output("Connected to default server")
            else:
                self._set_command_output("No server manager available")
            return
        if normalized in {"gallery", "open gallery", "open_gallery"}:
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.action_show_gallery()
                self._set_command_output("Opened gallery")
            return
        if normalized in {"command", "command prompt", "command_prompt", "open_command_prompt"}:
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.action_show_command_prompt()
                if isinstance(app.screen, CommandPromptScreen):
                    app.screen.set_output("Opened command prompt")
            return
        if normalized in {"quick actions", "open quick actions", "open_quick_actions"}:
            self._set_command_output("Quick actions are available on the dashboard")
            return

        if normalized in {"quit", "exit"}:
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.exit()
            return

        self._set_command_output(f"Unknown command: {command}")

    def _refresh_dashboard(self) -> None:
        app = self.app
        summary_widget: DashboardSummary = self.query_one(DashboardSummary)
        summary_widget.update_summary(
            self._build_summary(), last_update=self._format_timestamp(datetime.now())
        )

        actions_widget: QuickActionsMenu = self.query_one(QuickActionsMenu)
        actions_widget.update_actions(self._build_quick_actions())

        commands_widget: CommandPromptPanel = self.query_one(CommandPromptPanel)
        commands_widget.update_commands(self._build_command_prompt_commands())

        sessions_widget: SessionDetailsPanel = self.query_one(SessionDetailsPanel)
        sessions_widget.update_sessions(self._build_session_details())

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
        library_count = 0
        library_items = 0

        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            server_names = app.server_manager.get_all_server_names()
            for name in server_names:
                status = app.server_manager.get_server_status(name)
                if status.get("connected"):
                    connected_count += 1
                session_count += int(status.get("session_count", 0))
                library_count += int(status.get("library_count", 0))
                library_items += int(status.get("library_items", 0))

        return {
            "total_servers": len(server_names),
            "connected_servers": connected_count,
            "active_sessions": session_count,
            "total_libraries": library_count,
            "total_library_items": library_items,
        }

    def _build_session_details(self) -> list[dict[str, Any]]:
        app = self.app
        sessions: list[dict[str, Any]] = []

        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            for name in app.server_manager.get_all_server_names():
                status = app.server_manager.get_server_status(name)
                for entry in status.get("now_playing", []):
                    session_entry = entry.copy()
                    session_entry["server"] = name
                    sessions.append(session_entry)

        return sessions

    def _build_quick_actions(self) -> list[str]:
        return [
            "Refresh Dashboard",
            "Connect Default Server",
            "Open Gallery",
            "Open Command Prompt",
        ]

    def _build_command_prompt_commands(self) -> list[str]:
        return [
            "refresh",
            "connect_default",
            "open_gallery",
            "open_command_prompt",
            "quit",
        ]

    def _set_command_output(self, message: str) -> None:
        if self.app is not None and self.app.screen is not None:
            if isinstance(self.app.screen, CommandPromptScreen):
                self.app.screen.set_output(message)
                return
        panel: CommandPromptPanel = self.query_one(CommandPromptPanel)
        panel.set_output(message)

    @staticmethod
    def _format_timestamp(timestamp: datetime) -> str:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")


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

    CSS_PATH = "../ui/styles/plexiglass.tcss"
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
        (":", "show_command_prompt", "Command"),
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

    def action_show_command_prompt(self) -> None:
        """Open the command prompt modal screen."""
        commands = [
            "refresh",
            "connect_default",
            "open_gallery",
            "quit",
        ]
        self.push_screen(CommandPromptScreen(commands))

    def _handle_command_prompt_command(self, command: str) -> None:
        screen = self.get_screen("main")
        if isinstance(screen, MainScreen):
            screen._handle_command(command)

    def action_help(self) -> None:
        """Placeholder help action (Textual will handle help overlay)."""
        return None
