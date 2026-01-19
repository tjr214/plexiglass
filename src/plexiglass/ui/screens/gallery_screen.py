"""
Gallery Screen - Main UI for browsing and executing demos.

This screen provides the interface for navigating through demo categories,
selecting demos, viewing code examples, and executing demonstrations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Static

from plexiglass.services.undo_service import UndoService
from plexiglass.services.exceptions import ConnectionError
from plexiglass.ui.widgets.category_menu import CategoryMenu
from plexiglass.ui.widgets.code_viewer import CodeViewer
from plexiglass.ui.widgets.demo_list import DemoList
from plexiglass.ui.widgets.demo_parameters import DemoParameters
from plexiglass.ui.widgets.scrollable_results import ScrollableResults
from plexiglass.ui.widgets.run_demo_button import RunDemoButton
from plexiglass.ui.widgets.undo_button import UndoButton

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo
    from plexiglass.gallery.registry import DemoRegistry


class DemoPanel(Static):
    """Widget displaying selected demo information."""

    def __init__(self, **kwargs) -> None:
        """Initialize demo panel."""
        super().__init__(**kwargs)
        self.current_demo: BaseDemo | None = None
        self.add_class("demo-panel")

    def set_demo(self, demo: BaseDemo | None) -> None:
        """
        Set the currently displayed demo.

        Args:
            demo: Demo to display, or None to clear
        """
        self.current_demo = demo
        self.update(self.render())

    def render(self) -> str:
        """Render the demo panel."""
        if self.current_demo is None:
            return "Select a category and demo to view details"

        lines = [
            f"📋 {self.current_demo.name}",
            "",
            f"Description: {self.current_demo.description}",
            f"Category: {self.current_demo.category}",
            f"Type: {self.current_demo.operation_type}",
        ]

        return "\n".join(lines)


class GalleryScreen(Screen):
    """
    Screen for browsing and executing API gallery demos.

    The Gallery Screen provides:
    - Category navigation
    - Demo selection
    - Code examples
    - Demo execution
    - Results display
    """

    TITLE = "PlexiGlass API Gallery"
    CSS_PATH = "../styles/gallery.tcss"
    BINDINGS = [
        ("escape", "dismiss", "Back to Dashboard"),
        ("q", "dismiss", "Quit Gallery"),
        ("tab", "focus_next", "Next Panel"),
        ("shift+tab", "focus_previous", "Prev Panel"),
        ("r", "run_demo", "Run Demo"),
    ]

    def __init__(self, registry: DemoRegistry, **kwargs) -> None:
        """
        Initialize the Gallery Screen.

        Args:
            registry: DemoRegistry instance containing all demos
        """
        super().__init__(**kwargs)
        self.registry = registry
        self._selected_category: str | None = None
        self._selected_demo: BaseDemo | None = None
        self.undo_service = UndoService()
        self._demo_list_initialized = False

    @property
    def selected_category(self) -> str | None:
        """Get the currently selected category."""
        return self._selected_category

    @selected_category.setter
    def selected_category(self, category: str | None) -> None:
        """Set the currently selected category."""
        self._selected_category = category
        try:
            demo_list = self.query_one("#demo-list", DemoList)
            demos = self.registry.get_demos_by_category(category) if category else []
            demo_list.update_demos(demos)
        except Exception:
            return

    @property
    def selected_demo(self) -> BaseDemo | None:
        """Get the currently selected demo."""
        return self._selected_demo

    @selected_demo.setter
    def selected_demo(self, demo: BaseDemo | None) -> None:
        """Set the currently selected demo."""
        self._selected_demo = demo
        try:
            demo_panel = self.query_one("#demo-summary", DemoPanel)
            demo_panel.set_demo(demo)
            code_viewer = self.query_one("#code-viewer", CodeViewer)
            code_viewer.set_demo(demo)
            undo_button = self.query_one("#undo-button", UndoButton)
            undo_button.set_can_undo(self.undo_service.can_undo())
            run_button = self.query_one("#run-demo", RunDemoButton)
            run_button.set_enabled(demo is not None)
            params_panel = self.query_one("#demo-params", DemoParameters)
            defaults = self._get_demo_defaults(demo)
            params_panel.update_parameters(
                self._get_demo_param_defs(demo), defaults, self._get_demo_options(demo)
            )
            params_panel.refresh(layout=True)
            if demo is None:
                results_display = self.query_one("#results-display", ScrollableResults)
                results_display.set_results(None)
        except Exception:
            return

    def record_undo_snapshot(self, operation: str, restore_data: dict[str, object]) -> None:
        """Record an undo snapshot and enable the undo button."""
        self.undo_service.snapshot(operation, restore_data)
        try:
            undo_button = self.query_one("#undo-button", UndoButton)
            undo_button.set_can_undo(self.undo_service.can_undo())
        except Exception:
            return

    @staticmethod
    def _get_demo_param_defs(demo: BaseDemo | None) -> list[dict[str, object]]:
        if demo is None:
            return []
        return demo.get_parameters()

    def _get_demo_defaults(self, demo: BaseDemo | None) -> dict[str, object]:
        if demo is None:
            return {}
        param_defs = demo.get_parameters()
        defaults: dict[str, object] = {}
        server_manager = getattr(self.app, "server_manager", None)
        server = None
        if server_manager is not None:
            try:
                server = server_manager.connect_to_default()
            except Exception:
                server = None

        for param_def in param_defs:
            name = param_def.get("name")
            if name == "section_name" and server is not None:
                try:
                    sections = list(server.library.sections())
                    if sections:
                        defaults[name] = getattr(sections[0], "title", "")
                except Exception:
                    continue
            if name == "query":
                defaults[name] = ""
            if name == "limit":
                defaults[name] = param_def.get("default", 10)
        return defaults

    def _get_demo_options(self, demo: BaseDemo | None) -> dict[str, list[str]]:
        if demo is None:
            return {}
        options: dict[str, list[str]] = {}
        server_manager = getattr(self.app, "server_manager", None)
        if server_manager is None:
            return options
        try:
            server = server_manager.connect_to_default()
        except Exception:
            return options

        for param_def in demo.get_parameters():
            name = param_def.get("name")
            if name == "section_name":
                try:
                    sections = list(server.library.sections())
                    options[name] = [getattr(section, "title", "") for section in sections]
                except Exception:
                    continue
        return options

    def compose(self) -> ComposeResult:
        """Compose the Gallery Screen layout."""
        yield Header()

        with Horizontal(id="gallery-container"):
            yield CategoryMenu(self.registry, id="category-menu")
            yield DemoList([], id="demo-list")
            with Vertical(id="demo-panel"):
                yield DemoPanel(id="demo-summary")
                yield CodeViewer(id="code-viewer")
                yield DemoParameters(id="demo-params")
                yield ScrollableResults(id="results-display")
                yield RunDemoButton(id="run-demo")
                yield UndoButton(id="undo-button")

        yield Footer()

    def on_category_menu_category_selected(self, event: CategoryMenu.CategorySelected) -> None:
        """Handle category selection from the menu."""
        self.selected_category = event.category
        self.selected_demo = None

    def on_demo_list_demo_selected(self, event: DemoList.DemoSelected) -> None:
        """Handle demo selection from the list."""
        self.selected_demo = event.demo

    def on_mount(self) -> None:
        """Set initial focus for keyboard navigation."""
        try:
            self.query_one("#category-menu", CategoryMenu).focus()
        except Exception:
            return

    def perform_undo(self) -> None:
        """Perform undo and display snapshot details."""
        snapshot = self.undo_service.undo()
        try:
            undo_button = self.query_one("#undo-button", UndoButton)
            undo_button.set_can_undo(self.undo_service.can_undo())
            results_display = self.query_one("#results-display", ScrollableResults)
            if snapshot is None:
                results_display.set_results({"undo": "none"})
            else:
                results_display.set_results(
                    {"undo_operation": snapshot.operation, "restore_data": snapshot.restore_data}
                )
        except Exception:
            return

    def action_run_demo(self) -> None:
        """Run the currently selected demo and display results."""
        demo = self._selected_demo
        if demo is None:
            return

        results_display = self.query_one("#results-display", ScrollableResults)
        server = None
        app = self.app
        server_manager = getattr(app, "server_manager", None)
        if server_manager is not None:
            try:
                server = server_manager.connect_to_default()
            except ConnectionError as exc:
                results_display.set_results({"error": str(exc)})
                return

        params_panel = self.query_one("#demo-params", DemoParameters)
        params = params_panel.get_values()
        is_valid, error = demo.validate_params(params)
        if not is_valid:
            results_display.set_results({"error": error})
            return

        try:
            results = demo.execute(server, params)
        except Exception as exc:  # noqa: BLE001
            results_display.set_results({"error": str(exc)})
            return

        results_display.set_results(results)

    def on_undo_button_pressed(self, event: UndoButton.Pressed) -> None:
        """Handle UndoButton presses."""
        self.perform_undo()

    def on_run_demo_button_pressed(self, event: RunDemoButton.Pressed) -> None:
        """Handle RunDemoButton presses."""
        del event
        self.action_run_demo()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Fallback handler for run demo button clicks."""
        if event.button.id == "run-demo":
            self.action_run_demo()

    async def action_dismiss(self, result=None) -> None:
        """Dismiss the gallery screen."""
        self.app.pop_screen()
