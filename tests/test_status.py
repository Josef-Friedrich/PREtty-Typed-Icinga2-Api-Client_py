from pretiac.client import Client


def test_without_args(client: Client) -> None:
    result = client.status.list()
    assert isinstance(result["results"][0]["name"], str)


def test_icinga_application(client: Client) -> None:
    result = client.status.list("IcingaApplication")
    assert result["results"][0]["name"] == "IcingaApplication"
    assert (
        result["results"][0]["status"]["icingaapplication"]["app"]["node_name"]
        == "icinga-master"
    )
