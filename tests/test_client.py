from pretiac.client import Client


def test_client() -> None:
    client = Client("https://localhost:5665", "api", "password")
    assert client.username == "api"
    assert client.password == "password"
