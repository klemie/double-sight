"""Basic trend engine tests."""

from typing import Any

from trend_engine import __version__


def test_version() -> None:
    """Test that version is set."""
    assert __version__ == "0.1.0"


def test_sample_shots_fixture(sample_shots: list[dict[str, Any]]) -> None:
    """Test that sample shots fixture is valid."""
    assert len(sample_shots) == 2
    assert sample_shots[0]["club"] == "7i"
    assert sample_shots[0]["metrics"]["carry"] == 165.2

