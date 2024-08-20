from pretiac.client import Client


def test_client() -> None:
    client = Client("https://localhost:5665", "apiuser", "password")
    assert client.username == "apiuser"
    assert client.password == "password"


def test_get_services() -> None:
    client = Client("https://localhost:5665", "apiuser", "password")
    services = client.objects.list("Service")
    assert services[0]["type"] == "Service"
