"""
DemoParameters widget for PlexiGlass Gallery.

Displays parameter inputs for the selected demo.
"""

from __future__ import annotations

from typing import Any

from textual.containers import Vertical
from textual.widgets import Input, Label, Select


class DemoParameters(Vertical):
    """Widget for capturing demo parameters."""

    DEFAULT_CSS = """
    DemoParameters {
        border: round $primary;
        background: $panel;
        padding: 1;
        height: auto;
    }

    DemoParameters Label {
        color: $text-muted;
    }

    DemoParameters .param-field {
        margin: 0 0 1 0;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._param_defs: list[dict[str, Any]] = []
        self._param_values: dict[str, Any] = {}
        self._select_options: dict[str, list[str]] = {}
        self.add_class("demo-params")

    def update_parameters(
        self,
        param_defs: list[dict[str, Any]],
        values: dict[str, Any] | None = None,
        options: dict[str, list[str]] | None = None,
    ) -> None:
        """Update parameter definitions and pre-fill values."""
        self._param_defs = param_defs
        self._param_values = values or {}
        self._select_options = options or {}
        if self.is_mounted:
            self._rebuild_contents()

    def on_mount(self) -> None:
        self._rebuild_contents()

    def get_values(self) -> dict[str, Any]:
        """Return current parameter values from inputs."""
        values: dict[str, Any] = {}
        for param_def in self._param_defs:
            name = param_def["name"]
            widget_id = f"param-{name}"
            try:
                select_widget = self.query_one(f"#{widget_id}", Select)
                values[name] = select_widget.value
                continue
            except Exception:
                pass
            try:
                input_widget = self.query_one(f"#{widget_id}", Input)
                values[name] = input_widget.value
            except Exception:
                continue
        return values

    def _rebuild_contents(self) -> None:
        self.remove_children()
        self.mount(Label("Parameters", classes="param-title"))
        if not self._param_defs:
            self.mount(Label("No parameters required", classes="param-field"))
            return

        for param_def in self._param_defs:
            name = param_def["name"]
            required = param_def.get("required", False)
            label = param_def.get("description") or name
            suffix = " (required)" if required else ""
            self.mount(Label(f"{label}{suffix}"))

            widget_id = f"param-{name}"
            options = self._select_options.get(name)
            default = self._param_values.get(name, param_def.get("default", ""))
            if options:
                select_options = [(option, option) for option in options]
                if default is None or default == "":
                    default = select_options[0][0] if select_options else ""
                self.mount(
                    Select(select_options, value=default, id=widget_id, classes="param-field")
                )
            else:
                self.mount(Input(value=str(default) if default is not None else "", id=widget_id))
