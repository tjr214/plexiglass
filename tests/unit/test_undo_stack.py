"""
Tests for UndoStack data model.
"""

from __future__ import annotations

from plexiglass.models.undo_stack import UndoSnapshot, UndoStack


class TestUndoStack:
    """Unit tests for UndoStack behavior."""

    def test_undo_stack_starts_empty(self):
        stack = UndoStack(max_size=5)

        assert stack.can_undo is False
        assert stack.size == 0

    def test_undo_stack_push_pop_lifo(self):
        stack = UndoStack(max_size=5)
        first = UndoSnapshot(operation="first", restore_data={"value": 1})
        second = UndoSnapshot(operation="second", restore_data={"value": 2})

        stack.push(first)
        stack.push(second)

        assert stack.size == 2
        assert stack.pop() == second
        assert stack.pop() == first
        assert stack.pop() is None

    def test_undo_stack_enforces_max_size(self):
        stack = UndoStack(max_size=2)
        stack.push(UndoSnapshot(operation="one", restore_data={"value": 1}))
        stack.push(UndoSnapshot(operation="two", restore_data={"value": 2}))
        stack.push(UndoSnapshot(operation="three", restore_data={"value": 3}))

        assert stack.size == 2
        third = stack.pop()
        second = stack.pop()

        assert third is not None
        assert second is not None
        assert third.operation == "three"
        assert second.operation == "two"
