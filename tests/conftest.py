import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def snapshot_activities():
    """Snapshot and restore the in-memory `activities` dict around each test.

    This avoids cross-test pollution since `src.app.activities` is module-level state.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
