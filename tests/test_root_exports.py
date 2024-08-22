"""Test the functions from the root ``__init__.py``."""

from pretiac import get_client


def test_get_client() -> None:
    client = get_client()
    assert client.api_user == "apiuser"
