import pytest
from pretiac.client import Client
from pretiac.exceptions import Icinga2ApiException


class TestProcessCheckResult:
    def test_success(self, client: Client) -> None:
        result = client.actions.process_check_result(
            "Service", "Host1!ssh", 3, "SSH failed"
        )
        assert result["results"][0]["code"] == 200
        assert (
            result["results"][0]["status"]
            == "Successfully processed check result for object 'Host1!ssh'."
        )

    def test_failure(self, client: Client) -> None:
        with pytest.raises(Icinga2ApiException, match="No objects found."):
            client.actions.process_check_result(
                "Service", "Host1!unknown_service", 3, "Unknown Service"
            )
