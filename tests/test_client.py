from pretiac.client import Client


def test_client(client: Client) -> None:
    assert client.url == "https://localhost:5665"
    assert client.username == "apiuser"
    assert client.password == "password"


def test_get_services(client: Client) -> None:
    services = client.objects.list("Service")
    assert services[0]["type"] == "Service"
