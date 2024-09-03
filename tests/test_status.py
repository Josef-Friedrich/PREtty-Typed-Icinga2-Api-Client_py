from pretiac.raw_client import RawClient


def test_without_args(client: RawClient) -> None:
    result = client.status.list()
    for status in result["results"]:
        assert isinstance(status["name"], str)


def test_icinga_application(client: RawClient) -> None:
    result = client.status.list("IcingaApplication")
    assert result["results"][0]["name"] == "IcingaApplication"
    assert (
        result["results"][0]["status"]["icingaapplication"]["app"]["node_name"]
        == "icinga-master"
    )
