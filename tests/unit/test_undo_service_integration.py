"""
Integration tests for UndoService stacking behavior.
"""

from __future__ import annotations

from plexiglass.services.undo_service import UndoService


class TestUndoServiceIntegration:
    """Integration coverage for undo stack sizing."""

    def test_undo_service_respects_max_stack(self):
        service = UndoService(max_stack=2)

        service.snapshot("first", {"value": 1})
        service.snapshot("second", {"value": 2})
        service.snapshot("third", {"value": 3})

        peeked = service.peek()
        first = service.undo()
        second = service.undo()
        third = service.undo()

        assert peeked is not None
        assert first is not None
        assert second is not None
        assert peeked.operation == "third"
        assert first.operation == "third"
        assert second.operation == "second"
        assert third is None
