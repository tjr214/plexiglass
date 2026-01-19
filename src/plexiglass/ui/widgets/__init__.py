"""
UI widgets for PlexiGlass TUI.

This package contains custom Textual widgets used throughout the application.
"""

from plexiglass.ui.widgets.category_menu import CategoryMenu
from plexiglass.ui.widgets.code_viewer import CodeViewer
from plexiglass.ui.widgets.demo_list import DemoList
from plexiglass.ui.widgets.demo_parameters import DemoParameters
from plexiglass.ui.widgets.results_display import ResultsDisplay
from plexiglass.ui.widgets.run_demo_button import RunDemoButton
from plexiglass.ui.widgets.scrollable_results import ScrollableResults
from plexiglass.ui.widgets.undo_button import UndoButton

__all__ = [
    "CategoryMenu",
    "CodeViewer",
    "DemoList",
    "DemoParameters",
    "ResultsDisplay",
    "RunDemoButton",
    "ScrollableResults",
    "UndoButton",
]
