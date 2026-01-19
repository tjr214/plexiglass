"""
Undo service for PlexiGlass.
"""

from __future__ import annotations

from plexiglass.models.undo_stack import UndoSnapshot, UndoStack


class UndoService:
    """Service for managing undo snapshots."""

    def __init__(self, max_stack: int = 50) -> None:
        self._stack = UndoStack(max_size=max_stack)

    def snapshot(self, operation: str, restore_data: dict[str, object]) -> None:
        """Capture a snapshot before a write operation."""
        snapshot = UndoSnapshot(operation=operation, restore_data=restore_data)
        self._stack.push(snapshot)

    def undo(self) -> UndoSnapshot | None:
        """Pop the latest snapshot to restore state."""
        return self._stack.pop()

    def peek(self) -> UndoSnapshot | None:
        """Peek at the latest snapshot without removing it."""
        return self._stack.peek()

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._stack.can_undo
