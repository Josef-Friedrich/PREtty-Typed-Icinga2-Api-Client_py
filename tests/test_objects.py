from pretiac.client import Client


class TestCreate:
    def test_without_args(self, client: Client) -> None:
        client.objects.delete("Service", "Host1!custom-load", suppress_exception=True)
        result = client.objects.create(
            "Service",
            "Host1!custom-load",
            templates=["generic-service"],
            attrs={"check_command": "load", "check_interval": 1, "retry_interval": 1},
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"
