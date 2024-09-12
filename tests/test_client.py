from pretiac.client import CheckError, CheckResponse, Client
from pretiac.config import Config
from pretiac.object_types import Function
from pretiac.raw_client import RawClient


def test_config(client: Client) -> None:
    assert client.http_basic_username == "apiuser"


def test_api_enpoint_host_ip() -> None:
    client = Client(
        api_endpoint_host="127.0.0.1",
        api_endpoint_port=5665,
        http_basic_username="apiuser",
        http_basic_password="password",
    )
    host = client.get_host("Host1")
    assert host
    assert host.name == "Host1"


def test_client_setup() -> None:
    config = Config(
        api_endpoint_host="127.0.0.1",
        api_endpoint_port=1221,
        http_basic_username="u",
        http_basic_password="p",
    )
    client = Client(config_file=False, config=config)
    assert client.api_endpoint_host == "127.0.0.1"
    assert client.api_endpoint_port == 1221
    assert client.http_basic_username == "u"
    assert client.http_basic_password == "p"
    assert client.client_certificate is None
    assert client.client_private_key is None
    assert client.ca_certificate is None


class TestApiUser:
    def test_get_all(self, client: Client) -> None:
        # o = object
        o = client.get_api_users()[0]
        assert o.type == "ApiUser"
        assert o.password is None
        assert o.client_cn == "my-api-client"
        assert o.package == "_etc"
        assert o.active is True
        assert o.permissions == ["*"]
        assert o.paused is False

    def test_get(self, client: Client) -> None:
        result = client.get_api_user("apiuser")
        assert result.name == "apiuser"
        assert result.client_cn == "my-api-client"
        assert result.permissions == ["*"]


class TestCheckCommand:
    def test_get_all(self, client: Client) -> None:
        o = client.get_check_commands()[0]
        assert o.type == "CheckCommand"
        assert o.name == "ido"
        assert o.templates == ["ido", "ido-check-command"]
        assert o.version == 0.0
        assert o.timeout == 60
        assert o.execute == Function(
            type="Function",
            name="Internal#IdoCheck",
            side_effect_free=False,
            deprecated=False,
            arguments=["checkable", "cr", "resolvedMacros", "useResolvedMacros"],
        )


class TestDependency:
    def test_get_all(self, client: Client) -> None:
        o = client.get_dependencys()[0]
        assert o.type == "Dependency"
        assert o.name == "Host2!Service2!Service1-Service2"
        assert o.type == "Dependency"
        assert o.templates == ["Service1-Service2"]
        assert o.parent_host_name == "Host1"
        assert o.parent_service_name == "Service1"
        assert o.child_host_name == "Host2"
        assert o.child_service_name == "Service2"
        assert o.redundancy_group is None
        assert o.disable_checks is True
        assert o.disable_notifications is True
        assert o.ignore_soft_states is True
        assert o.period is None
        assert o.states == ["OK", "Warning"]


class TestEndpoint:
    def test_get_all(self, client: Client) -> None:
        o = client.get_endpoints()[0]
        assert o.type == "Endpoint"
        assert o.name == "icinga-master"
        assert o.source_location
        assert o.source_location.path == "/etc/icinga2/zones.conf"
        assert o.log_duration == 86400


class TestHost:
    class TestCreate:
        def test_only_name(self, client: Client) -> None:
            name = "MyNewHost"
            client.delete_host(name)
            host = client.create_host(name)
            assert host
            assert host.name == name
            client.delete_host(name)

        def test_display_name(self, client: Client) -> None:
            name = "MyNewHost"
            display_name = "My display name"
            client.delete_host(name)
            host = client.create_host(name, display_name=display_name)
            assert host
            assert host.display_name == display_name
            client.delete_host(name)

    class TestGet:
        def test_success(self, client: Client) -> None:
            host = client.get_host("Host1")
            assert host
            assert host.name == "Host1"
            assert host.notes is None

        def test_none(self, client: Client) -> None:
            host = client.get_host("unknown")
            assert host is None

    def test_get_all(self, client: Client) -> None:
        o = client.get_hosts()
        assert len(o) > 2


class TestService:
    class TestCreateService:
        def test_create_service(self, client: Client, raw_client: RawClient) -> None:
            service = "MyNewService"
            host = "Host1"
            client.delete_service(host=host, service=service)
            client.create_service(service, host)
            assert (
                client.get_service(host=host, service=service).name
                == f"{host}!{service}"
            )
            client.delete_service(host=host, service=service)

        def test_name_with_spaces(self, client: Client) -> None:
            service = "rsync host:/data/ssd/ /ssd/"
            host = "Host1"
            client.delete_service(host=host, service=service)
            client.create_service(service, host)
            assert (
                client.get_service(host=host, service=service).name
                == f"{host}!{service}"
            )
            client.delete_service(host=host, service=service)

        def test_display_name(self, client: Client) -> None:
            client.delete_service(host="Host1", service="short_name")
            client.create_service(
                "short_name", "Host1", display_name="Nice display name"
            )
            service = client.get_service(host="Host1", service="short_name")
            assert service.name == "Host1!short_name"
            assert service.display_name == "Nice display name"
            client.delete_service(host="Host1", service="short_name")

    class TestSendServiceCheckResult:
        def test_success(self, client: Client) -> None:
            result = client.send_service_check_result(
                service="ssh",
                host="Host1",
                exit_status=2,
                plugin_output="test",
                create=False,
            )
            assert isinstance(result, CheckResponse)
            assert (
                result.status
                == "Successfully processed check result for object 'Host1!ssh'."
            )
            assert result.code == 200

        def test_error(self, client: Client, raw_client: RawClient) -> None:
            raw_client.objects.delete(
                "Service", "Host1!unknown", suppress_exception=True
            )

            result = client.send_service_check_result(
                service="unknown",
                host="Host1",
                exit_status=2,
                plugin_output="test",
                create=False,
            )
            assert isinstance(result, CheckError)
            assert result.status == "No objects found."
            assert result.error == 404

        def test_send_service_check_result_safe(
            self, client: Client, raw_client: RawClient
        ) -> None:
            raw_client.objects.delete(
                "Service", "NewHost!NewService", suppress_exception=True
            )
            raw_client.objects.delete("Host", "NewHost", suppress_exception=True)

            result = client.send_service_check_result(
                service="NewService",
                host="NewHost",
                exit_status=2,
                plugin_output="test",
            )
            assert isinstance(result, CheckResponse)
            assert (
                result.status
                == "Successfully processed check result for object 'NewHost!NewService'."
            )
            assert result.code == 200

            raw_client.objects.delete(
                "Service", "NewHost!NewService", suppress_exception=True
            )
            raw_client.objects.delete("Host", "NewHost", suppress_exception=True)

    def test_get_all(self, client: Client) -> None:
        o = client.get_services()[0]
        assert isinstance(o.name, str)
        assert o.type == "Service"


class TestTimePeriod:
    def test_get_all(self, client: Client) -> None:
        o = client.get_time_periods()[0]
        assert isinstance(o.name, str)
        assert o.type == "TimePeriod"


class TestUser:
    def test_get_all(self, client: Client) -> None:
        o = client.get_users()[0]
        assert isinstance(o.name, str)
        assert o.type == "User"


class TestUserGroup:
    def test_get_all(self, client: Client) -> None:
        o = client.get_user_groups()[0]
        assert isinstance(o.name, str)
        assert o.type == "UserGroup"


class TestZone:
    def test_get_all(self, client: Client) -> None:
        o = client.get_zones()[0]
        assert isinstance(o.name, str)
        assert o.type == "Zone"


class TestVariables:
    def test_get_all(self, client: Client) -> None:
        v = client.get_variables()[0]
        assert isinstance(v.name, str)
        assert isinstance(v.type, str)
        assert v.value
