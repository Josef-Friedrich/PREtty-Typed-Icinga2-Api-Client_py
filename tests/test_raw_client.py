from pretiac.raw_client import RawClient


class TestClient:
    def test_domain(self, raw_client: RawClient) -> None:
        assert raw_client.config.api_endpoint_host == "localhost"

    def test_port(self, raw_client: RawClient) -> None:
        assert raw_client.config.api_endpoint_port == 5665

    def test_url(self, raw_client: RawClient) -> None:
        assert raw_client.url == "https://localhost:5665"

    def test_api_user(self, raw_client: RawClient) -> None:
        assert raw_client.config.http_basic_username == "apiuser"

    def test_password(self, raw_client: RawClient) -> None:
        assert raw_client.config.http_basic_password == "password"

    def test_version(self, raw_client: RawClient) -> None:
        assert isinstance(raw_client.version, str)


def test_get_services(raw_client: RawClient) -> None:
    services = raw_client.objects.list("Service")
    assert services[0]["type"] == "Service"
