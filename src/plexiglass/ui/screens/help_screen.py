"""
Help Screen - Comprehensive searchable help with keyboard shortcuts.
"""

from textual.screen import Screen
from textual.widgets import Static, Input, ListView, ListItem, Label
from textual.containers import Container, Vertical, Horizontal
from textual.reactive import reactive
from plexiglass.services.help_content import HelpContent


class HelpScreen(Screen):
    """
    Help screen with searchable topics and keyboard shortcuts.

    Features:
    - Topic list navigation
    - Search functionality
    - Content display
    - Keyboard shortcuts reference
    - Context-sensitive help
    """

    BINDINGS = [
        ("escape", "dismiss", "Close Help"),
        ("q", "dismiss", "Close Help"),
    ]

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    
    .help-container {
        width: 90%;
        height: 90%;
        background: $panel;
        border: tall $accent;
        padding: 1 2;
    }
    
    .help-header {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
        text-align: center;
    }
    
    .help-search {
        margin-bottom: 1;
    }
    
    .help-content-area {
        layout: horizontal;
        height: 100%;
    }
    
    .help-topic-list {
        width: 30%;
        height: 100%;
        border: tall $primary;
        padding: 1;
        margin-right: 1;
    }
    
    .help-content-display {
        width: 70%;
        height: 100%;
        border: tall $primary;
        padding: 1 2;
        overflow-y: scroll;
    }
    
    .help-topic-title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    
    .help-topic-category {
        color: $text-muted;
        text-style: italic;
        margin-bottom: 1;
    }
    """

    # Reactive properties
    search_query = reactive("")
    current_topic = reactive("overview")
    initial_topic = reactive(None)

    def __init__(self, initial_topic: str = None, **kwargs):
        """
        Initialize HelpScreen.

        Args:
            initial_topic: Initial topic to display
        """
        super().__init__(**kwargs)
        self.initial_topic = initial_topic or "overview"
        self.current_topic = self.initial_topic
        self.help_content = HelpContent()
        self.topic_list = None
        self.content_display = None

    def compose(self):
        """Compose the help screen."""
        with Container(classes="help-container"):
            yield Static("📚 PlexiGlass Help", classes="help-header")

            yield Input(
                placeholder="Search help topics...", classes="help-search", id="help-search-input"
            )

            with Horizontal(classes="help-content-area"):
                # Topic list
                with Vertical(classes="help-topic-list"):
                    yield Static("Topics:", classes="help-topic-title")
                    yield ListView(id="topic-list")

                # Content display
                with Vertical(classes="help-content-display"):
                    yield Static(id="content-display")

    def on_mount(self):
        """Handle mount event - populate topics."""
        self.topic_list = self.query_one("#topic-list", ListView)
        self.content_display = self.query_one("#content-display", Static)

        self._populate_topics()
        self._display_topic(self.current_topic)

    def _populate_topics(self):
        """Populate topic list."""
        topics = self.help_content.get_all_topics()

        self.topic_list.clear()
        for topic in topics:
            item = ListItem(Label(topic["title"]), id=f"topic-{topic['id']}")
            self.topic_list.append(item)

    def on_input_changed(self, event: Input.Changed):
        """Handle search input change."""
        if event.input.id == "help-search-input":
            self.search_topics(event.value)

    def on_list_view_selected(self, event: ListView.Selected):
        """Handle topic selection."""
        if event.list_view.id == "topic-list":
            topic_id = event.item.id.replace("topic-", "")
            self.select_topic(topic_id)

    def select_topic(self, topic_id: str):
        """
        Select and display a topic.

        Args:
            topic_id: Topic identifier
        """
        self.current_topic = topic_id
        self._display_topic(topic_id)

    def _display_topic(self, topic_id: str):
        """Display topic content."""
        topic = self.help_content.get_topic(topic_id)

        if topic and self.content_display:
            content = f"[bold]{topic['title']}[/bold]\n"
            content += f"[dim italic]{topic['category']}[/dim italic]\n\n"
            content += topic["content"]

            self.content_display.update(content)

    def search_topics(self, query: str):
        """
        Search and filter topics.

        Args:
            query: Search query
        """
        self.search_query = query
        results = self.help_content.search(query)

        if self.topic_list:
            self.topic_list.clear()
            for topic in results:
                item = ListItem(Label(topic["title"]), id=f"topic-{topic['id']}")
                self.topic_list.append(item)

    def clear_search(self):
        """Clear search and show all topics."""
        self.search_query = ""
        if self.topic_list:
            try:
                search_input = self.query_one("#help-search-input", Input)
                search_input.value = ""
            except Exception:
                pass
            self._populate_topics()

    def action_dismiss(self):
        """Dismiss the help screen."""
        self.dismiss()
