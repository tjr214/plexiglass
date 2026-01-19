"""
Tests for UndoService behavior.
"""

from __future__ import annotations

from plexiglass.services.undo_service import UndoService


class TestUndoService:
    """Unit tests for UndoService."""

    def test_undo_service_starts_empty(self):
        service = UndoService(max_stack=5)

        assert service.can_undo() is False
        assert service.peek() is None

    def test_undo_service_records_snapshot(self):
        service = UndoService(max_stack=5)

        service.snapshot("update", {"item_id": 1, "original": "old"})

        assert service.can_undo() is True
        snapshot = service.peek()
        assert snapshot is not None
        assert snapshot.operation == "update"

    def test_undo_service_undo_returns_snapshot(self):
        service = UndoService(max_stack=5)
        service.snapshot("update", {"item_id": 1})
        service.snapshot("delete", {"item_id": 2})

        snapshot = service.undo()

        assert snapshot is not None
        assert snapshot.operation == "delete"
        assert service.can_undo() is True

    def test_undo_service_undo_empty_returns_none(self):
        service = UndoService(max_stack=5)

        assert service.undo() is None
