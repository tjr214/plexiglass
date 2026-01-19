"""
Tests for loading state widgets (LoadingIndicator and ProgressBar).
"""

import pytest
from textual.app import App
from plexiglass.ui.widgets.loading_indicator import LoadingIndicator
from plexiglass.ui.widgets.progress_bar import ProgressBar


class TestLoadingIndicator:
    """Test suite for LoadingIndicator widget."""

    @pytest.mark.asyncio
    async def test_loading_indicator_creation(self):
        """Test LoadingIndicator can be created."""
        indicator = LoadingIndicator()
        assert indicator is not None

    @pytest.mark.asyncio
    async def test_loading_indicator_with_message(self):
        """Test LoadingIndicator with custom message."""
        indicator = LoadingIndicator(message="Loading data...")
        assert indicator.message == "Loading data..."

    @pytest.mark.asyncio
    async def test_loading_indicator_default_message(self):
        """Test LoadingIndicator with default message."""
        indicator = LoadingIndicator()
        assert indicator.message == "Loading..."

    @pytest.mark.asyncio
    async def test_loading_indicator_is_animating(self):
        """Test LoadingIndicator animating state."""
        indicator = LoadingIndicator()
        assert indicator.is_animating is True

    @pytest.mark.asyncio
    async def test_loading_indicator_stop_animation(self):
        """Test stopping LoadingIndicator animation."""
        indicator = LoadingIndicator()
        indicator.stop()
        assert indicator.is_animating is False

    @pytest.mark.asyncio
    async def test_loading_indicator_start_animation(self):
        """Test starting LoadingIndicator animation."""
        indicator = LoadingIndicator()
        indicator.stop()
        assert indicator.is_animating is False
        indicator.start()
        assert indicator.is_animating is True

    @pytest.mark.asyncio
    async def test_loading_indicator_has_css_classes(self):
        """Test LoadingIndicator applies CSS classes."""
        indicator = LoadingIndicator()
        assert "loading-indicator" in indicator.classes

    @pytest.mark.asyncio
    async def test_loading_indicator_update_message(self):
        """Test updating LoadingIndicator message."""
        indicator = LoadingIndicator(message="Initial")
        indicator.update_message("Updated")
        assert indicator.message == "Updated"


class TestProgressBar:
    """Test suite for ProgressBar widget."""

    @pytest.mark.asyncio
    async def test_progress_bar_creation(self):
        """Test ProgressBar can be created."""
        bar = ProgressBar()
        assert bar is not None
        assert bar.progress == 0
        assert bar.total == 100

    @pytest.mark.asyncio
    async def test_progress_bar_with_total(self):
        """Test ProgressBar with custom total."""
        bar = ProgressBar(total=50)
        assert bar.total == 50
        assert bar.progress == 0

    @pytest.mark.asyncio
    async def test_progress_bar_initial_progress(self):
        """Test ProgressBar with initial progress."""
        bar = ProgressBar(progress=25, total=100)
        assert bar.progress == 25
        assert bar.total == 100

    @pytest.mark.asyncio
    async def test_progress_bar_update(self):
        """Test updating ProgressBar progress."""
        bar = ProgressBar(total=100)
        bar.update(50)
        assert bar.progress == 50

    @pytest.mark.asyncio
    async def test_progress_bar_increment(self):
        """Test incrementing ProgressBar."""
        bar = ProgressBar(total=100)
        bar.increment(10)
        assert bar.progress == 10
        bar.increment(15)
        assert bar.progress == 25

    @pytest.mark.asyncio
    async def test_progress_bar_percentage(self):
        """Test ProgressBar percentage calculation."""
        bar = ProgressBar(progress=25, total=100)
        assert bar.percentage == 25.0

        bar.update(50)
        assert bar.percentage == 50.0

        bar.update(100)
        assert bar.percentage == 100.0

    @pytest.mark.asyncio
    async def test_progress_bar_percentage_zero_total(self):
        """Test ProgressBar percentage with zero total."""
        bar = ProgressBar(total=0)
        assert bar.percentage == 0.0

    @pytest.mark.asyncio
    async def test_progress_bar_complete(self):
        """Test ProgressBar completion detection."""
        bar = ProgressBar(total=100)
        assert bar.is_complete is False

        bar.update(100)
        assert bar.is_complete is True

    @pytest.mark.asyncio
    async def test_progress_bar_reset(self):
        """Test resetting ProgressBar."""
        bar = ProgressBar(total=100)
        bar.update(75)
        assert bar.progress == 75

        bar.reset()
        assert bar.progress == 0

    @pytest.mark.asyncio
    async def test_progress_bar_with_label(self):
        """Test ProgressBar with label."""
        bar = ProgressBar(label="Downloading...")
        assert bar.label == "Downloading..."

    @pytest.mark.asyncio
    async def test_progress_bar_update_label(self):
        """Test updating ProgressBar label."""
        bar = ProgressBar(label="Initial")
        bar.update_label("Updated")
        assert bar.label == "Updated"

    @pytest.mark.asyncio
    async def test_progress_bar_show_percentage(self):
        """Test ProgressBar show percentage option."""
        bar = ProgressBar(show_percentage=True)
        assert bar.show_percentage is True

        bar_no_pct = ProgressBar(show_percentage=False)
        assert bar_no_pct.show_percentage is False

    @pytest.mark.asyncio
    async def test_progress_bar_clamp_to_total(self):
        """Test ProgressBar clamps progress to total."""
        bar = ProgressBar(total=100)
        bar.update(150)  # Try to exceed total
        assert bar.progress == 100  # Should clamp to total

    @pytest.mark.asyncio
    async def test_progress_bar_negative_progress(self):
        """Test ProgressBar prevents negative progress."""
        bar = ProgressBar(total=100)
        bar.update(-10)  # Try negative
        assert bar.progress == 0  # Should clamp to 0

    @pytest.mark.asyncio
    async def test_progress_bar_has_css_classes(self):
        """Test ProgressBar applies CSS classes."""
        bar = ProgressBar()
        assert "progress-bar" in bar.classes
