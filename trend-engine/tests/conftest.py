"""Pytest fixtures for trend engine tests."""

from typing import Any

import pytest


@pytest.fixture
def sample_shots() -> list[dict[str, Any]]:
    """Sample shot data for testing."""
    return [
        {
            "id": "shot-001",
            "captured_at": "2025-12-23T10:00:00Z",
            "club": "7i",
            "metrics": {
                "carry": 165.2,
                "offline": -3.1,
                "ball_speed": 118.4,
                "spin": 6200,
            },
            "session_id": "session-001",
            "is_outlier": False,
        },
        {
            "id": "shot-002",
            "captured_at": "2025-12-23T10:01:00Z",
            "club": "7i",
            "metrics": {
                "carry": 162.8,
                "offline": 1.2,
                "ball_speed": 116.9,
                "spin": 6400,
            },
            "session_id": "session-001",
            "is_outlier": False,
        },
    ]
