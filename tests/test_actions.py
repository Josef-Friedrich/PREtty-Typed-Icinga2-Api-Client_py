import pytest

from pretiac.client import Client
from pretiac.exceptions import PretiacException


class TestProcessCheckResult:
    def test_success(self, client: Client) -> None:
        result = client.actions.process_check_result(
            "Service", "Host1!ssh", 2, "SSH failed"
        )
        assert len(result["results"]) == 1
        assert result["results"][0]["code"] == 200
        assert (
            result["results"][0]["status"]
            == "Successfully processed check result for object 'Host1!ssh'."
        )

        service = client.objects.get("Service", "Host1!ssh")
        assert service["attrs"]["state"] == 2

        client.actions.process_check_result("Service", "Host1!ssh", 0, "SSH failed")

        service = client.objects.get("Service", "Host1!ssh")
        assert service["attrs"]["state"] == 0

    def test_failure_unknown_service(self, client: Client) -> None:
        with pytest.raises(PretiacException, match="No objects found."):
            client.actions.process_check_result(
                "Service", "Host1!unknown_service", 3, "Unknown Service"
            )

    def test_failure_unknown_host_unknown_service(self, client: Client) -> None:
        result = client.actions.process_check_result(
            "Service",
            "UnknownHost!unknown_service",
            3,
            "Unknown Service",
            suppress_exception=True,
        )
        assert result["error"] == 404
        assert result["status"] == "No objects found."
