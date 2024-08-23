"""Test the functions from the root ``__init__.py``."""

from pretiac import CheckError, CheckResult, get_client, send_service_check_result


def test_get_client() -> None:
    client = get_client()
    assert client.config.api_user == "apiuser"


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
