from pretiac.client import CheckError, CheckResult, Client
from pretiac.raw_client import RawClient


def test_config(client: Client) -> None:
    assert client.config.http_basic_username == "apiuser"


class TestHost:
    def test_create(self, client: Client, raw_client: RawClient) -> None:
        raw_client.objects.delete("Host", "MyNewHost", suppress_exception=True)
        client.create_host("MyNewHost")
        host = raw_client.objects.get("Host", "MyNewHost")
        assert host["name"] == "MyNewHost"

    def test_get(self, client: Client) -> None:
        host = client.get_host("Host1")
        assert host.name == "Host1"


class TestService:
    class TestCreateService:
        def test_create_service(self, client: Client, raw_client: RawClient) -> None:
            service = "MyNewService"
            host = "Host1"
            client.delete_service(host=host, service=service)
            client.create_service(service, host)
            assert (
                client.get_service(host=host, service=service).name
                == f"{host}!{service}"
            )
            client.delete_service(host=host, service=service)

        def test_name_with_spaces(self, client: Client) -> None:
            service = "rsync host:/data/ssd/ /ssd/"
            host = "Host1"
            client.delete_service(host=host, service=service)
            client.create_service(service, host)
            assert (
                client.get_service(host=host, service=service).name
                == f"{host}!{service}"
            )
            client.delete_service(host=host, service=service)

        def test_display_name(self, client: Client) -> None:
            client.delete_service(host="Host1", service="short_name")
            client.create_service(
                "short_name", "Host1", display_name="Nice display name"
            )
            service = client.get_service(host="Host1", service="short_name")
            assert service.name == "Host1!short_name"
            assert service.display_name == "Nice display name"
            client.delete_service(host="Host1", service="short_name")

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
            raw_client.objects.delete(
                "Service", "Host1!unknown", suppress_exception=True
            )

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
                service="NewService",
                host="NewHost",
                exit_status=2,
                plugin_output="test",
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

    def test_get_services(self, client: Client) -> None:
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
