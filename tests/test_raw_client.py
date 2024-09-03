from pretiac.raw_client import RawClient


class TestClient:
    def test_domain(self, client: RawClient) -> None:
        assert client.config.api_endpoint_host == "localhost"

    def test_port(self, client: RawClient) -> None:
        assert client.config.api_endpoint_port == 5665

    def test_url(self, client: RawClient) -> None:
        assert client.url == "https://localhost:5665"

    def test_api_user(self, client: RawClient) -> None:
        assert client.config.http_basic_username == "apiuser"

    def test_password(self, client: RawClient) -> None:
        assert client.config.http_basic_password == "password"

    def test_version(self, client: RawClient) -> None:
        assert isinstance(client.version, str)


def test_get_services(client: RawClient) -> None:
    services = client.objects.list("Service")
    assert services[0]["type"] == "Service"
