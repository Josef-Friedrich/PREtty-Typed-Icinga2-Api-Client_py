from pretiac.raw_client import RawClient


def test_without_args(raw_client: RawClient) -> None:
    result = raw_client.status.list()
    for status in result["results"]:
        assert isinstance(status["name"], str)


def test_icinga_application(raw_client: RawClient) -> None:
    result = raw_client.status.list("IcingaApplication")
    assert result["results"][0]["name"] == "IcingaApplication"
    assert (
        result["results"][0]["status"]["icingaapplication"]["app"]["node_name"]
        == "icinga-master"
    )
