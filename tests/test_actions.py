from pretiac.client import Client


def test_client(client: Client) -> None:
    result = client.actions.process_check_result(
        "Service", "Host1!ssh", 3, "SSH failed"
    )
    assert result["results"][0]["code"] == 200
    assert (
        result["results"][0]["status"]
        == "Successfully processed check result for object 'Host1!ssh'."
    )
