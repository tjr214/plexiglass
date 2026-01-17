"""Configuration for pytest."""

import pytest


@pytest.fixture
def sample_fixture():
    """Sample fixture for demonstration."""
    return "sample_data"
