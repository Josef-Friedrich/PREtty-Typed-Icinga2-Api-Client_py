from __future__ import annotations

import pytest

from pretiac.client import Client


@pytest.fixture
def client() -> Client:
    return Client("https://localhost:5665", "apiuser", "password")
