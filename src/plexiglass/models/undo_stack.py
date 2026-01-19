"""
Undo stack model for PlexiGlass.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UndoSnapshot:
    """Represents a single undo snapshot."""

    operation: str
    restore_data: dict[str, object]


class UndoStack:
    """Stack for managing undo snapshots."""

    def __init__(self, max_size: int = 50) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._items: list[UndoSnapshot] = []

    @property
    def size(self) -> int:
        return len(self._items)

    @property
    def can_undo(self) -> bool:
        return bool(self._items)

    def push(self, snapshot: UndoSnapshot) -> None:
        """Push a snapshot onto the stack, enforcing max size."""
        self._items.append(snapshot)
        if len(self._items) > self._max_size:
            self._items = self._items[-self._max_size :]

    def pop(self) -> UndoSnapshot | None:
        """Pop the most recent snapshot or return None if empty."""
        if not self._items:
            return None
        return self._items.pop()

    def peek(self) -> UndoSnapshot | None:
        """Peek at the latest snapshot without removing it."""
        if not self._items:
            return None
        return self._items[-1]
