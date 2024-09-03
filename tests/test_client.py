from pretiac.client import CheckError, CheckResult, Client
from pretiac.raw_client import RawClient


def test_config(client: Client) -> None:
    assert client.config.http_basic_username == "apiuser"


def test_create_host(client: Client, raw_client: RawClient) -> None:
    raw_client.objects.delete("Host", "MyNewHost", suppress_exception=True)
    client.create_host("MyNewHost")
    host = raw_client.objects.get("Host", "MyNewHost")
    assert host["name"] == "MyNewHost"


class TestCreateService:
    def test_create_service(self, client: Client, raw_client: RawClient) -> None:
        raw_client.objects.delete("Service", "MyNewService", suppress_exception=True)
        client.create_service("MyNewService", "Host1")
        service = raw_client.objects.get("Service", "Host1!MyNewService")
        assert service["name"] == "Host1!MyNewService"
        raw_client.objects.delete("Service", "MyNewService", suppress_exception=True)

    def test_name_with_spaces(self, client: Client, raw_client: RawClient) -> None:
        name = "rsync host:/data/ssd/ /ssd/"
        raw_client.objects.delete("Service", name, suppress_exception=True)
        client.create_service(name, "Host1")
        service = raw_client.objects.get("Service", f"Host1!{name}")
        assert service["name"] == f"Host1!{name}"
        raw_client.objects.delete("Service", name, suppress_exception=True)


class TestSendServiceCheckResult:
    def test_success(self, client: Client) -> None:
        result = client.send_service_check_result(
            service="ssh",
            host="Host1",
            exit_status=2,
            plugin_output="test",
            create=False,
        )
        assert isinstance(result, CheckResult)
        assert (
            result.status
            == "Successfully processed check result for object 'Host1!ssh'."
        )
        assert result.code == 200

    def test_error(self, client: Client, raw_client: RawClient) -> None:
        raw_client.objects.delete("Service", "Host1!unknown", suppress_exception=True)

        result = client.send_service_check_result(
            service="unknown",
            host="Host1",
            exit_status=2,
            plugin_output="test",
            create=False,
        )
        assert isinstance(result, CheckError)
        assert result.status == "No objects found."
        assert result.error == 404

    def test_send_service_check_result_safe(
        self, client: Client, raw_client: RawClient
    ) -> None:
        raw_client.objects.delete(
            "Service", "NewHost!NewService", suppress_exception=True
        )
        raw_client.objects.delete("Host", "NewHost", suppress_exception=True)

        result = client.send_service_check_result(
            service="NewService", host="NewHost", exit_status=2, plugin_output="test"
        )
        assert isinstance(result, CheckResult)
        assert (
            result.status
            == "Successfully processed check result for object 'NewHost!NewService'."
        )
        assert result.code == 200

        raw_client.objects.delete(
            "Service", "NewHost!NewService", suppress_exception=True
        )
        raw_client.objects.delete("Host", "NewHost", suppress_exception=True)


def test_get_services(
    client: Client,
) -> None:
    results = client.get_services()
    assert isinstance(results[0].name, str)
    assert results[0].type == "Service"


def test_get_time_periods(client: Client) -> None:
    results = client.get_time_periods()
    assert isinstance(results[0].name, str)
    assert results[0].type == "TimePeriod"


def test_get_users(client: Client) -> None:
    results = client.get_users()
    assert isinstance(results[0].name, str)
    assert results[0].type == "User"


def test_get_api_users(client: Client) -> None:
    results = client.get_api_users()
    assert isinstance(results[0].name, str)
    assert results[0].type == "ApiUser"


def test_get_api_user(client: Client) -> None:
    result = client.get_api_user("apiuser")
    assert result.name == "apiuser"
    assert result.password is None
    assert result.client_cn == "my-api-client"
    assert result.permissions == ["*"]
