"""
DemoList widget for PlexiGlass Gallery.

Displays demos for the selected category.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

if TYPE_CHECKING:
    from plexiglass.gallery.base_demo import BaseDemo


class DemoList(VerticalScroll):
    """Widget for navigating demos within a category."""

    DEFAULT_CSS = """
    DemoList {
        border: round $primary;
        background: $panel;
        padding: 1;
        width: 36;
        height: 100%;
    }

    DemoList > ListView {
        background: transparent;
        border: none;
    }

    DemoList > ListView > ListItem {
        padding: 0 1;
        height: auto;
    }

    DemoList > ListView > ListItem:hover {
        background: $primary-darken-2;
    }

    DemoList > ListView > ListItem.-selected {
        background: $primary;
        color: $text;
    }

    DemoList Label {
        color: $text-muted;
        text-align: center;
        padding: 2;
    }
    """

    class DemoSelected(Message):
        """Message emitted when a demo is selected."""

        def __init__(self, demo: BaseDemo) -> None:
            super().__init__()
            self.demo = demo

    def __init__(self, demos: list[BaseDemo], **kwargs) -> None:
        super().__init__(**kwargs)
        self._demos = demos
        self._demo_map: dict[int, BaseDemo] = {}
        self.add_class("demo-list")

    def update_demos(self, demos: list[BaseDemo]) -> None:
        """Update the demos displayed in the list."""
        self._demos = demos
        self._demo_map = {}
        list_view = self.query_one(ListView)
        list_view.clear()

        if not demos:
            list_view.append(ListItem(Label("No demos in this category")))
            return

        for index, demo in enumerate(demos):
            list_item = ListItem(Label(demo.name))
            self._demo_map[index] = demo
            list_view.append(list_item)

        list_view.index = 0

    def compose(self) -> ComposeResult:
        if not self._demos:
            yield ListView(ListItem(Label("Select a category")), id="demo-list-view")
            return

        items = [ListItem(Label(demo.name)) for demo in self._demos]
        for index, demo in enumerate(self._demos):
            self._demo_map[index] = demo
        yield ListView(*items, id="demo-list-view")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_view = event.list_view
        index = list_view.index
        if index is not None and index in self._demo_map:
            demo = self._demo_map[index]
            self.post_message(self.DemoSelected(demo))
