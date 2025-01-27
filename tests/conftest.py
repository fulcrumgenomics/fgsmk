from pathlib import Path

import pytest


@pytest.fixture
def datadir() -> Path:
    """Return a path to the test data directory."""
    return Path(__file__).parent / "data"
