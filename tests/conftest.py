from __future__ import annotations

from pathlib import Path

import pytest

from pretiac.client import Client


@pytest.fixture
def config_file() -> Path:
    path = Path(__file__).parent / ".." / "resources" / "icinga-api-client.json"
    return path.resolve()


@pytest.fixture
def client() -> Client:
    return Client("https://localhost:5665", "apiuser", "password")
