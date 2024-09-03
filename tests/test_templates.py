from pretiac.raw_client import RawClient


def test_host(client: RawClient) -> None:
    result = client.templates.list("Host")
    template = result["results"][0]
    assert template["name"] == "generic-host"
    assert template["type"] == "Host"


def test_service(client: RawClient) -> None:
    result = client.templates.list("Service")
    template = result["results"][0]
    assert template["name"] == "generic-service"
    assert template["type"] == "Service"


class TestFilter:
    def test_match(self, client: RawClient) -> None:
        result = client.templates.list("Service", 'match("generic*", tmpl.name)')
        assert len(result["results"]) == 1

    def test_no_match(self, client: RawClient) -> None:
        result = client.templates.list("Service", 'match("unknown*", tmpl.name)')
        assert len(result["results"]) == 0
