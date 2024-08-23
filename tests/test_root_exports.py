"""Test the functions from the root ``__init__.py``."""

from pretiac import (
    CheckError,
    CheckResult,
    create_host,
    create_service,
    get_client,
    send_service_check_result,
    send_service_check_result_safe,
)
from pretiac.client import Client


def test_get_client() -> None:
    client = get_client()
    assert client.config.api_user == "apiuser"


def test_create_host(client: Client) -> None:
    client.objects.delete("Host", "MyNewHost", suppress_exception=True)
    create_host("MyNewHost")
    host = client.objects.get("Host", "MyNewHost")
    assert host["name"] == "MyNewHost"


def test_create_service(client: Client) -> None:
    client.objects.delete("Service", "MyNewService", suppress_exception=True)
    create_service("MyNewService", "Host1")
    host = client.objects.get("Service", "Host1!MyNewService")
    assert host["name"] == "Host1!MyNewService"


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
