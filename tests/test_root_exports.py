"""Test the functions from the root ``__init__.py``."""

from pretiac import (
    CheckError,
    CheckResult,
    create_host,
    create_service,
    get_client,
    get_services,
    get_time_periods,
    get_users,
    send_service_check_result,
    send_service_check_result_safe,
)
from pretiac.client import Client


def test_get_client() -> None:
    client = get_client()
    assert client.config.http_basic_username == "apiuser"


def test_create_host(client: Client) -> None:
    client.objects.delete("Host", "MyNewHost", suppress_exception=True)
    create_host("MyNewHost")
    host = client.objects.get("Host", "MyNewHost")
    assert host["name"] == "MyNewHost"


class TestCreateService:
    def test_create_service(self, client: Client) -> None:
        client.objects.delete("Service", "MyNewService", suppress_exception=True)
        create_service("MyNewService", "Host1")
        service = client.objects.get("Service", "Host1!MyNewService")
        assert service["name"] == "Host1!MyNewService"
        client.objects.delete("Service", "MyNewService", suppress_exception=True)

    def test_name_with_spaces(self, client: Client) -> None:
        name = "rsync host:/data/ssd/ /ssd/"
        client.objects.delete("Service", name, suppress_exception=True)
        create_service(name, "Host1")
        service = client.objects.get("Service", f"Host1!{name}")
        assert service["name"] == f"Host1!{name}"
        client.objects.delete("Service", name, suppress_exception=True)


class TestSendServiceCheckResult:
    def test_success(self) -> None:
        result = send_service_check_result("Host1", "ssh", 2, "test")
        assert isinstance(result, CheckResult)
        assert (
            result.status
            == "Successfully processed check result for object 'Host1!ssh'."
        )
        assert result.code == 200

    def test_error(self) -> None:
        result = send_service_check_result(
            "Host1", "unknown", 2, "test", suppress_exception=True
        )
        assert isinstance(result, CheckError)
        assert result.status == "No objects found."
        assert result.error == 404


def test_send_service_check_result_safe(client: Client) -> None:
    client.objects.delete("Service", "NewHost!NewService", suppress_exception=True)
    client.objects.delete("Host", "NewHost", suppress_exception=True)

    result = send_service_check_result_safe("NewHost", "NewService", 2, "test")
    assert isinstance(result, CheckResult)
    assert (
        result.status
        == "Successfully processed check result for object 'NewHost!NewService'."
    )
    assert result.code == 200

    client.objects.delete("Service", "NewHost!NewService", suppress_exception=True)
    client.objects.delete("Host", "NewHost", suppress_exception=True)


def test_get_services() -> None:
    results = get_services()
    assert isinstance(results[0].name, str)
    assert results[0].type == "Service"


def test_get_time_periods() -> None:
    results = get_time_periods()
    assert isinstance(results[0].name, str)
    assert results[0].type == "TimePeriod"


def test_get_users() -> None:
    results = get_users()
    assert isinstance(results[0].name, str)
    assert results[0].type == "User"
