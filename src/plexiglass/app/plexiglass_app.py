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

import yaml
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from plexapi.server import PlexServer
from textual.widgets import Button, Checkbox, Footer, Header, Input, Static

from plexiglass.config.loader import ConfigLoader
from plexiglass.gallery.registry import DemoRegistry
from plexiglass.gallery.demos.collections.list_collections import ListCollectionsDemo
from plexiglass.gallery.demos.collections.list_playlists import ListPlaylistsDemo
from plexiglass.gallery.demos.library.list_library_items import ListLibraryItemsDemo
from plexiglass.gallery.demos.library.list_library_sections import ListLibrarySectionsDemo
from plexiglass.gallery.demos.library.search_library import SearchLibraryDemo
from plexiglass.gallery.demos.media.list_artists import ListArtistsDemo
from plexiglass.gallery.demos.media.list_movies import ListMoviesDemo
from plexiglass.gallery.demos.media.list_shows import ListShowsDemo
from plexiglass.gallery.demos.myp.account_details import MyPlexAccountDetailsDemo
from plexiglass.gallery.demos.myp.list_devices import MyPlexDevicesDemo
from plexiglass.gallery.demos.playback.list_play_queues import ListPlayQueuesDemo
from plexiglass.gallery.demos.playback.list_playback_sessions import ListPlaybackSessionsDemo
from plexiglass.gallery.demos.playback.list_recent_plays import ListRecentPlaysDemo
from plexiglass.gallery.demos.server.get_server_info import GetServerInfoDemo
from plexiglass.gallery.demos.server.list_server_clients import ListServerClientsDemo
from plexiglass.gallery.demos.server.list_server_libraries import ListServerLibrariesDemo
from plexiglass.gallery.demos.server.list_server_sessions import ListServerSessionsDemo
from plexiglass.gallery.demos.settings.list_server_preferences import ListServerPreferencesDemo
from plexiglass.gallery.demos.settings.list_server_settings import ListServerSettingsDemo
from plexiglass.gallery.demos.users.list_shared_libraries import ListSharedLibrariesDemo
from plexiglass.gallery.demos.users.list_users import ListUsersDemo
from plexiglass.gallery.demos.search.global_search import GlobalSearchDemo
from plexiglass.gallery.demos.search.hub_search import HubSearchDemo
from plexiglass.gallery.demos.search.get_recommendations import GetRecommendationsDemo
from plexiglass.gallery.demos.sync.list_sync_items import ListSyncItemsDemo
from plexiglass.gallery.demos.sync.get_sync_status import GetSyncStatusDemo
from plexiglass.gallery.demos.alerts.list_activity_alerts import ListActivityAlertsDemo
from plexiglass.gallery.demos.alerts.monitor_timeline import MonitorTimelineDemo
from plexiglass.gallery.demos.integrations.discover_sonos import DiscoverSonosDemo
from plexiglass.gallery.demos.integrations.list_integrations import ListIntegrationsDemo
from plexiglass.gallery.demos.analysis.get_media_streams import GetMediaStreamsDemo
from plexiglass.gallery.demos.analysis.analyze_codec_info import AnalyzeCodecInfoDemo
from plexiglass.gallery.demos.utilities.get_download_url import GetDownloadURLDemo
from plexiglass.gallery.demos.utilities.get_thumbnail_url import GetThumbnailURLDemo
from plexiglass.gallery.demos.advanced.get_server_capabilities import GetServerCapabilitiesDemo
from plexiglass.gallery.demos.advanced.list_server_activities import ListServerActivitiesDemo
from plexiglass.services.server_manager import ServerManager
from plexiglass.ui.screens.gallery_screen import GalleryScreen


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

    def __init__(self, actions: list[dict[str, str]], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.actions = actions
        self.add_class("quick-actions")

    def compose(self) -> ComposeResult:
        yield Static("Quick Actions", classes="section-title")
        for action in self.actions:
            yield Button(action["label"], id=f"action-{action['key']}")

    def update_actions(self, actions: list[dict[str, str]]) -> None:
        self.actions = actions
        # Actions are static; avoid remount to prevent duplicate IDs.

    def trigger_action(self, action_key: str) -> None:
        self.post_message(self.ActionTriggered(action_key))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("action-"):
            action_key = event.button.id.replace("action-", "")
            self.trigger_action(action_key)

    class ActionTriggered(Message):
        """Message fired when a quick action is triggered."""

        bubble = True

        def __init__(self, action_key: str) -> None:
            super().__init__()
            self.action_key = action_key


class CommandPromptPanel(Static):
    """Popup command prompt panel for dashboard actions."""

    def __init__(self, commands: list[dict[str, str]], **kwargs: Any) -> None:
        super().__init__("", **kwargs)
        self.commands = commands
        self.last_output: str | None = None
        self.add_class("command-prompt")

    def on_mount(self) -> None:
        self.update(self._render_prompt())

    def update_commands(self, commands: list[dict[str, str]]) -> None:
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
            lines.extend(f"- {command['key']}" for command in self.commands)
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

    def __init__(self, commands: list[dict[str, str]], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.commands = commands
        self.history: list[str] = []
        self.last_output: str | None = None
        self.command_keys = [command["key"] for command in commands]

    def compose(self) -> ComposeResult:
        with Container(classes="command-modal"):
            yield Static("Command Prompt", classes="modal-title")
            if self.commands:
                yield Static("Commands:", classes="modal-section")
                with Vertical(id="command-list"):
                    for command in self.commands:
                        yield Button(command["label"], id=f"cmd-{command['key']}")
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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("cmd-"):
            command_key = event.button.id.replace("cmd-", "")
            self.submit_command(command_key)

    def _update_suggestions(self, text: str) -> None:
        normalized = text.strip().lower()
        matches = [
            command for command in self.command_keys if command.lower().startswith(normalized)
        ]
        if not normalized:
            matches = self.command_keys
        if not matches:
            suggestions = "No suggestions"
        else:
            suggestions = self._format_grouped_suggestions(matches)
        self.query_one("#command-suggestions", Static).update(suggestions)

    def _format_grouped_suggestions(self, commands: list[str]) -> str:
        grouped: dict[str, list[str]] = {}
        help_map = self._command_help()
        for command in commands:
            group = help_map.get(command, {}).get("group", "Other")
            grouped.setdefault(group, []).append(command)

        lines: list[str] = []
        all_commands = sum(len(values) for values in grouped.values())
        page_size = 10
        visible = 0
        for group in sorted(grouped.keys()):
            group_commands = sorted(grouped[group])
            if visible >= page_size:
                break
            lines.append(f"{group}")
            for command in group_commands:
                if visible >= page_size:
                    break
                lines.append(f"  {self._format_command_help(command)}")
                visible += 1

        if all_commands > page_size:
            lines.append(f"Showing {visible} of {all_commands} commands")

        return "\n".join(lines)

    def _format_command_help(self, command: str) -> str:
        command_help = self._command_help().get(command, {})
        description = command_help.get("description", "Run command")
        return f"{command} - {description}"

    @staticmethod
    def _command_help() -> dict[str, dict[str, str]]:
        return {
            "refresh": {
                "description": "Refresh dashboard data",
                "group": "Core",
            },
            "connect_default": {
                "description": "Connect to default server",
                "group": "Core",
            },
            "open_gallery": {
                "description": "Open gallery screen",
                "group": "Navigation",
            },
            "open_command_prompt": {
                "description": "Show command prompt modal",
                "group": "Navigation",
            },
            "list_servers": {
                "description": "List configured servers",
                "group": "Info",
            },
            "list_libraries": {
                "description": "List libraries across servers",
                "group": "Info",
            },
            "disconnect": {
                "description": "Disconnect from all servers",
                "group": "Core",
            },
            "edit_config": {
                "description": "Edit server configuration",
                "group": "Navigation",
            },
            "quit": {
                "description": "Exit the application",
                "group": "System",
            },
        }

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
        normalized = self._resolve_command(command)
        main_screen = None
        if isinstance(self.app, PlexiGlassApp):
            main_screen = self.app.get_screen("main")
            if isinstance(main_screen, MainScreen) and isinstance(main_screen.app, PlexiGlassApp):
                main_screen.app.server_manager = self.app.server_manager

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
        if normalized in {"disconnect", "disconnect_all", "disconnect all"}:
            app = self.app
            if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
                for name in app.server_manager.get_connected_servers():
                    app.server_manager.disconnect_server(name)
                self._set_command_output("Disconnected from all servers")
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
        if normalized in {"edit_config", "edit config", "config"}:
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.action_edit_config()
            return
        if normalized in {"quick actions", "open quick actions", "open_quick_actions"}:
            self._set_command_output("Quick actions are available on the dashboard")
            return

        if normalized.startswith("list_servers") or normalized == "servers":
            app = self.app
            filter_value = normalized.replace("list_servers", "").strip()
            server_manager = self._resolve_server_manager(app, main_screen)

            if server_manager is not None:
                if filter_value in {"connected", "online"}:
                    connected = server_manager.get_connected_servers()
                    names = sorted([str(name) for name in connected])
                else:
                    names = server_manager.get_all_server_names()
                if names:
                    output = "Servers:\n" + "\n".join(f"- {name}" for name in names)
                else:
                    output = "No servers configured"
                self._set_command_output(output)
            else:
                self._set_command_output("No server manager available")
            return

        if normalized.startswith("list_libraries") or normalized == "libraries":
            app = self.app
            server_manager = self._resolve_server_manager(app, main_screen)
            if server_manager is not None:
                names: list[str] = []
                for server_name in server_manager.get_all_server_names():
                    status = server_manager.get_server_status(server_name)
                    names.extend(status.get("library_names", []))
                unique_names = sorted({name for name in names})
                if unique_names:
                    output = "Libraries:\n" + "\n".join(f"- {name}" for name in unique_names)
                else:
                    output = "No libraries found"
                self._set_command_output(output)
            else:
                self._set_command_output("No server manager available")
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

    def _build_quick_actions(self) -> list[dict[str, str]]:
        return [
            {"key": "refresh", "label": "Refresh Dashboard"},
            {"key": "connect_default", "label": "Connect Default Server"},
            {"key": "open_gallery", "label": "Open Gallery"},
            {"key": "open_command_prompt", "label": "Open Command Prompt"},
            {"key": "edit_config", "label": "Edit Server Config"},
        ]

    def _build_command_prompt_commands(self) -> list[dict[str, str]]:
        return [
            {"key": "refresh", "label": "Refresh dashboard data"},
            {"key": "connect_default", "label": "Connect to default server"},
            {"key": "disconnect", "label": "Disconnect all servers"},
            {"key": "open_gallery", "label": "Open gallery screen"},
            {"key": "open_command_prompt", "label": "Show command prompt"},
            {"key": "edit_config", "label": "Edit server config"},
            {"key": "list_servers", "label": "List configured servers"},
            {"key": "list_libraries", "label": "List libraries across servers"},
            {"key": "quit", "label": "Exit application"},
        ]

    def _set_command_output(self, message: str) -> None:
        if self.app is not None and self.app.screen is not None:
            if isinstance(self.app.screen, CommandPromptScreen):
                self.app.screen.set_output(message)
                return
        panel: CommandPromptPanel = self.query_one(CommandPromptPanel)
        panel.set_output(message)

    def _resolve_command(self, command: str) -> str:
        normalized = command.strip().lower()
        matches = [
            action["key"]
            for action in self._build_command_prompt_commands()
            if action["key"].startswith(normalized)
        ]
        return matches[0] if matches else normalized

    @staticmethod
    def _resolve_server_manager(
        app: App[object] | None, main_screen: Screen | None
    ) -> ServerManager | None:
        if isinstance(app, PlexiGlassApp) and app.server_manager is not None:
            return app.server_manager
        if isinstance(main_screen, MainScreen) and isinstance(main_screen.app, PlexiGlassApp):
            return main_screen.app.server_manager
        return None

    @staticmethod
    def _format_timestamp(timestamp: datetime) -> str:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")


class ConfigSetupPromptScreen(Screen):
    """Blocking prompt shown when configuration is missing or invalid."""

    def __init__(self, config_path: Path, error_message: str | None = None, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.config_path = config_path
        self.error_message = error_message

    def compose(self) -> ComposeResult:
        with Container(classes="config-prompt"):
            yield Static("Configuration Required", classes="modal-title")
            yield Static(
                "No valid server configuration was found. PlexiGlass needs a server config to run.",
                classes="modal-body",
            )
            if self.error_message:
                yield Static(f"Error: {self.error_message}", classes="modal-error")
            yield Static(f"Target file: {self.config_path}", classes="modal-body")
            with Horizontal(classes="modal-actions"):
                yield Button("Create Config", id="create-config")
                yield Button("Quit", id="quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-config":
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.push_screen(app._build_config_setup_screen())
        elif event.button.id == "quit":
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.exit()


class ConfigSetupScreen(Screen):
    """Multi-server configuration builder screen."""

    def __init__(self, config_path: Path, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.config_path = config_path
        self.server_entries: list[dict[str, Any]] = []
        self.error_message: str | None = None

    def compose(self) -> ComposeResult:
        with Container(classes="config-builder"):
            yield Static("Server Configuration", classes="modal-title")
            yield Static(
                "Add one or more Plex servers. Tokens can be found in Plex Web by viewing XML for a media item and copying X-Plex-Token from the URL.",
                classes="modal-body",
            )
            yield Static("Server List:", classes="modal-section")
            yield Static("", id="server-list")
            with Container(classes="form-row"):
                yield Input(placeholder="Server URL (http://host:32400)", id="server-url")
            with Container(classes="form-row"):
                yield Input(placeholder="Token", id="server-token")
            with Container(classes="form-row"):
                yield Input(placeholder="Description (optional)", id="server-description")
            with Container(classes="form-row"):
                yield Checkbox(label="Default server", id="server-default")
            yield Static(
                "Token help: Sign in to Plex Web, open any media item XML, copy X-Plex-Token from the URL.",
                classes="modal-body",
            )
            yield Static("", id="setup-error", classes="modal-error")
            with Horizontal(classes="modal-actions"):
                yield Button("Validate & Add", id="add-server")
                yield Button("Save Config", id="save-config")
                yield Button("Cancel", id="cancel-config")

    def add_server(self, server: dict[str, Any]) -> None:
        if server.get("default"):
            for entry in self.server_entries:
                entry["default"] = False
        self.server_entries.append(server)
        self._render_server_list()

    def save_config(self) -> None:
        settings = ConfigLoader._get_default_settings()
        payload = {
            "servers": self.server_entries,
            "settings": settings,
        }
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    def load_from_config(self) -> None:
        if not self.config_path.exists():
            return
        try:
            raw_config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        except Exception:
            return
        if not isinstance(raw_config, dict):
            return
        servers = raw_config.get("servers", [])
        if isinstance(servers, list):
            self.server_entries = [server for server in servers if isinstance(server, dict)]
            self._render_server_list()

    def _render_server_list(self) -> None:
        lines = []
        for server in self.server_entries:
            default = " (default)" if server.get("default") else ""
            lines.append(f"- {server.get('name', 'Unknown')}{default}")
        self.query_one("#server-list", Static).update("\n".join(lines))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-server":
            self._handle_add_server()
        elif event.button.id == "save-config":
            self._handle_save()
        elif event.button.id == "cancel-config":
            app = self.app
            if isinstance(app, PlexiGlassApp):
                app.exit()

    def _handle_add_server(self) -> None:
        self.error_message = None
        url = self.query_one("#server-url", Input).value.strip()
        token = self.query_one("#server-token", Input).value.strip()
        description = self.query_one("#server-description", Input).value.strip()
        default_value = self.query_one("#server-default", Checkbox).value

        if not url or not token:
            self._set_error("URL and token are required.")
            return

        try:
            server_name = self._validate_server(url, token)
        except Exception as exc:  # noqa: BLE001
            self._set_error(str(exc))
            return

        self.add_server(
            {
                "name": server_name,
                "description": description or "",
                "url": url,
                "token": token,
                "default": default_value,
                "read_only": False,
                "ssl_verify": True,
                "tags": [],
            }
        )
        self.query_one("#server-url", Input).value = ""
        self.query_one("#server-token", Input).value = ""
        self.query_one("#server-description", Input).value = ""
        self.query_one("#server-default", Checkbox).value = False

    def _handle_save(self) -> None:
        if not self.server_entries:
            self._set_error("Add at least one server before saving.")
            return
        self.save_config()
        app = self.app
        if isinstance(app, PlexiGlassApp):
            app._load_configuration()
            app.switch_screen("main")

    def _set_error(self, message: str) -> None:
        self.error_message = message
        self.query_one("#setup-error", Static).update(message)

    @staticmethod
    def _validate_server(url: str, token: str) -> str:
        server = PlexServer(baseurl=url, token=token)
        return server.friendlyName


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
        self.config_path = config_path or (Path.home() / ".config" / "plexiglass" / "servers.yaml")
        self.config_loader: ConfigLoader | None = None
        self.server_manager: ServerManager | None = None
        self.error_message: str | None = None

    def on_mount(self) -> None:
        """Initialize services and screens when app mounts."""
        self._load_configuration()
        if self.config_loader is None:
            self.push_screen(
                ConfigSetupPromptScreen(self.config_path, error_message=self.error_message)
            )
        else:
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
        registry = self._build_demo_registry()
        screen = GalleryScreen(registry)
        self.push_screen(screen)

    def action_show_main(self) -> None:
        """Switch to the Main screen."""
        self.switch_screen("main")

    def action_show_command_prompt(self) -> None:
        """Open the command prompt modal screen."""
        main_screen = self.get_screen("main")
        commands: list[dict[str, str]] = []
        if isinstance(main_screen, MainScreen):
            commands = main_screen._build_command_prompt_commands()
        self.push_screen(CommandPromptScreen(commands))

    def action_edit_config(self) -> None:
        """Open config builder for editing existing config."""
        setup_screen = self._build_config_setup_screen()
        self.push_screen(setup_screen)
        self.call_later(setup_screen.load_from_config)

    def _handle_command_prompt_command(self, command: str) -> None:
        screen = self.get_screen("main")
        if isinstance(screen, MainScreen):
            screen._handle_command(command)

    def _build_config_setup_screen(self) -> ConfigSetupScreen:
        return ConfigSetupScreen(self.config_path)

    @staticmethod
    def _build_demo_registry() -> DemoRegistry:
        registry = DemoRegistry()
        registry.register(GetServerInfoDemo)
        registry.register(ListServerSessionsDemo)
        registry.register(ListServerClientsDemo)
        registry.register(ListServerLibrariesDemo)
        registry.register(ListLibrarySectionsDemo)
        registry.register(ListLibraryItemsDemo)
        registry.register(SearchLibraryDemo)
        registry.register(ListMoviesDemo)
        registry.register(ListShowsDemo)
        registry.register(ListArtistsDemo)
        registry.register(ListPlayQueuesDemo)
        registry.register(ListPlaybackSessionsDemo)
        registry.register(ListRecentPlaysDemo)
        registry.register(ListCollectionsDemo)
        registry.register(ListPlaylistsDemo)
        registry.register(ListUsersDemo)
        registry.register(ListSharedLibrariesDemo)
        registry.register(MyPlexAccountDetailsDemo)
        registry.register(MyPlexDevicesDemo)
        registry.register(ListServerSettingsDemo)
        registry.register(ListServerPreferencesDemo)
        registry.register(GlobalSearchDemo)
        registry.register(HubSearchDemo)
        registry.register(GetRecommendationsDemo)
        registry.register(ListSyncItemsDemo)
        registry.register(GetSyncStatusDemo)
        registry.register(ListActivityAlertsDemo)
        registry.register(MonitorTimelineDemo)
        registry.register(DiscoverSonosDemo)
        registry.register(ListIntegrationsDemo)
        registry.register(GetMediaStreamsDemo)
        registry.register(AnalyzeCodecInfoDemo)
        registry.register(GetDownloadURLDemo)
        registry.register(GetThumbnailURLDemo)
        registry.register(GetServerCapabilitiesDemo)
        registry.register(ListServerActivitiesDemo)
        return registry

    def action_help(self) -> None:
        """Placeholder help action (Textual will handle help overlay)."""
        return None
