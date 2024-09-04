"""
A high level client with typed return values.
"""

import socket
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, TypeAdapter

from pretiac.config import Config, ObjectConfig, load_config
from pretiac.exceptions import PretiacException
from pretiac.log import logger
from pretiac.object_types import ApiUser, Host, Service, ServiceState, TimePeriod, User
from pretiac.raw_client import RawClient, StatusMessage
from pretiac.request_handler import Payload, State


def _normalize_object_config(
    templates: Optional[Sequence[str] | str] = None,
    attrs: Optional[Payload] = None,
    object_config: Optional[ObjectConfig] = None,
) -> ObjectConfig:
    """
    :param templates: Import existing configuration templates for this
        object type. Note: These templates must either be statically
        configured or provided in config packages.
    :param attrs: Set specific object attributes for this object type.
    :param object_config: Bundle of all configurations required to create an object.
    """
    if attrs is None and object_config is not None and object_config.attrs is not None:
        attrs = object_config.attrs

    if (
        templates is None
        and object_config is not None
        and object_config.templates is not None
    ):
        templates = object_config.templates

    if isinstance(templates, str):
        templates = [templates]

    return ObjectConfig(attrs=attrs, templates=templates)


def _convert_object(result: Any, type: Any) -> Any:
    if result is None:
        return None
    adapter = TypeAdapter(type)
    attrs = result["attrs"]
    if "__name" in attrs:
        attrs["name"] = attrs["__name"]
        del attrs["__name"]
    return adapter.validate_python(attrs)


class CheckResult(BaseModel):
    code: int
    status: str


class CheckError(BaseModel):
    error: int
    status: str


def _get_host(host: Optional[str] = None) -> str:
    if host is None:
        host = socket.gethostname()
    return host


def _get_service_name(
    name: Optional[str] = None,
    service: Optional[str] = None,
    host: Optional[str] = None,
) -> str:
    if name is not None:
        return name

    if service is not None and host is not None:
        return f"{host}!{service}"

    raise PretiacException("The service name could not be assembled!")


class Client:
    """The high level client with typed output.

    It is a wrapper around the :class:`RawClient`.
    """

    raw_client: RawClient

    config: Config

    def __init__(
        self,
        config_file: Optional[str | Path] = None,
        api_endpoint_host: Optional[str] = None,
        api_endpoint_port: Optional[int] = None,
        http_basic_username: Optional[str] = None,
        http_basic_password: Optional[str] = None,
        client_private_key: Optional[str] = None,
        client_certificate: Optional[str] = None,
        ca_certificate: Optional[str] = None,
        suppress_exception: Optional[bool] = None,
    ) -> None:
        """
        :param config_file: The path of the configuration file to load.
        :param api_endpoint_host: The domain or the IP address of the API
            endpoint, e. g. ``icinga.example.com``, ``localhost`` or ``127.0.0.1``.
        :param api_endpoint_port: The TCP port of the API endpoint, for example
            ``5665``.
        :param http_basic_username: The name of the API user used in the HTTP basic
            authentification, e. g. ``apiuser``.
        :param http_basic_password: The password of the API user used in the HTTP
            basic authentification, e. g. ``password``.
        :param client_private_key: The file path of the client’s **private RSA
            key**, for example ``/etc/pretiac/api-client.key.pem``.
        :param client_certificate: The file path of the client’s **certificate**,
            for example ``/etc/pretiac/api-client.cert.pem``.
        :param ca_certificate: The file path of the Icinga **CA (Certification
            Authority)**, for example ``/var/lib/icinga2/certs/ca.crt``.
        :param suppress_exception: If set to ``True``, no exceptions are thrown.
        """
        self.config = load_config(
            config_file=config_file,
            api_endpoint_host=api_endpoint_host,
            api_endpoint_port=api_endpoint_port,
            http_basic_username=http_basic_username,
            http_basic_password=http_basic_password,
            client_private_key=client_private_key,
            client_certificate=client_certificate,
            ca_certificate=ca_certificate,
            suppress_exception=suppress_exception,
        )
        self.raw_client = RawClient(self.config)

    def _get_objects(self, type: Any) -> Sequence[Any]:
        results = self.raw_client.objects.list(type.__name__)
        objects: list[type] = []
        for result in results:
            objects.append(_convert_object(result, type))
        return objects

    def _get_object(self, type: Any, name: str) -> Any:
        return _convert_object(
            self.raw_client.objects.get(
                object_type=type.__name__, name=name, suppress_exception=True
            ),
            type,
        )

    # Listed in the same order as in this `Markdown document <https://github.com/Icinga/icinga2/blob/master/doc/09-object-types.md>`__.

    # CRUD: create_object get_object get_objects delete_object

    # api_user #########################################################################

    def get_api_user(self, name: str) -> ApiUser:
        return self._get_object(ApiUser, name)

    def get_api_users(self) -> Sequence[ApiUser]:
        return self._get_objects(ApiUser)

    # host #############################################################################

    def create_host(
        self,
        name: str,
        display_name: Optional[str] = None,
        templates: Optional[Sequence[str]] = None,
        attrs: Optional[Payload] = None,
        object_config: Optional[ObjectConfig] = None,
        suppress_exception: Optional[bool] = None,
    ) -> Optional[Host]:
        """
        Create a new host. If no host configuration is specified, the template
        ``generic-host`` is assigned.

        :param name: The name of the host.
        :param display_name: A short description of the host.
        :param templates: Import existing configuration templates for this
            object type. Note: These templates must either be statically
            configured or provided in config packages.
        :param attrs: Set specific object attributes for this object type.
        :param object_config: Bundle of all configurations required to create a host.
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        The method call

        .. code-block::

            client.create_host(name='framework')

        creates for example a configuration file in the location
        ``/var/lib/icinga2/api/packages/_api/33d433c5-2c2f-4159-84fc-41395ddcd04d/conf.d/hosts/framework.conf``
        with the content:

        .. code-block::

            object Host "framework" {
                import "generic-host"

                version = 1725393956.244954
                zone = "master"
            }
        """
        config = _normalize_object_config(
            templates=templates, attrs=attrs, object_config=object_config
        )

        if config.attrs is None and config.templates is None:
            config.templates = ["generic-host"]

        if display_name is not None:
            if config.attrs is None:
                config.attrs = {}
            config.attrs["display_name"] = display_name

        logger.info("Create host %s", name)

        self.raw_client.objects.create(
            "Host",
            name,
            templates=config.templates,
            attrs=config.attrs,
            suppress_exception=suppress_exception,
        )
        return self.get_host(name=name)

    def get_host(self, name: str) -> Optional[Host]:
        """
        Get a single host.

        :param name: The name of the host.
        """
        return self._get_object(Host, name)

    def get_hosts(self) -> Sequence[Host]:
        """Get all hosts."""
        return self._get_objects(Host)

    def delete_host(self, name: str) -> None:
        """Delete a single host.

        :param name: The name of the host."""
        self.raw_client.objects.delete(
            "Host",
            name,
            suppress_exception=True,
        )

    # service ##########################################################################

    def create_service(
        self,
        name: str,
        host: str,
        display_name: Optional[str] = None,
        templates: Optional[Sequence[str]] = None,
        attrs: Optional[Payload] = None,
        object_config: Optional[ObjectConfig] = None,
        suppress_exception: Optional[bool] = None,
    ) -> None:
        """
        Create a new service. If no service configuration is specified, the dummy check
        command is assigned.

        :param name: The name of the service.
        :param host: The name of the host.
        :param display_name: A short description of the service.
        :param templates: Import existing configuration templates for this
            object type. Note: These templates must either be statically
            configured or provided in config packages.
        :param attrs: Set specific object attributes for this object type.
        :param object_config: Bundle of all configurations required to create a service.
        :param suppress_exception: If this parameter is set to ``True``, no exceptions are thrown.

        .. code-block::

            client.create_service(name='procs_zombie', host='framework', display_name='Zombie processes')

        Creates a configuration file like
        ``/var/lib/icinga2/api/packages/_api/33d433c5-2c2f-4159-84fc-41395ddcd04d/conf.d/services/framework!procs_zombie.conf``
        this one:

        .. code-block::

            object Service "procs_zombie" {
                check_command = "dummy"
                display_name = "Zombie processes"
                host_name = "framework"
                version = 1725393956.973319
                zone = "master"
            }
        """
        config = _normalize_object_config(
            templates=templates, attrs=attrs, object_config=object_config
        )

        if config.attrs is None and config.templates is None:
            config.attrs = {"check_command": "dummy"}

        if display_name is not None:
            if config.attrs is None:
                config.attrs = {}
            config.attrs["display_name"] = display_name

        logger.info("Create service %s", name)

        self.raw_client.objects.create(
            "Service",
            f"{host}!{name}",
            templates=config.templates,
            attrs=config.attrs,
            suppress_exception=suppress_exception,
        )

    def get_service(
        self,
        name: Optional[str] = None,
        host: Optional[str] = None,
        service: Optional[str] = None,
    ) -> Service:
        """
        :param name: The full name of the service, for example ``host!service``.
        :param host: The name of the host.
        :param service: The name of the service.
        """
        return self._get_object(
            Service, _get_service_name(name=name, service=service, host=host)
        )

    def get_services(self) -> Sequence[Service]:
        return self._get_objects(Service)

    def delete_service(
        self,
        name: Optional[str] = None,
        host: Optional[str] = None,
        service: Optional[str] = None,
    ) -> None:
        """
        :param name: The full name of the service, for example ``host!service``.
        :param host: The name of the host.
        :param service: The name of the service.
        """
        self.raw_client.objects.delete(
            "Service",
            _get_service_name(name=name, service=service, host=host),
            suppress_exception=True,
        )

    def send_service_check_result(
        self,
        service: str,
        host: Optional[str] = None,
        exit_status: Optional[State] = ServiceState.OK,
        plugin_output: Optional[str] = None,
        performance_data: Optional[Sequence[str] | str] = None,
        check_command: Optional[Sequence[str] | str] = None,
        check_source: Optional[str] = None,
        execution_start: Optional[float] = None,
        execution_end: Optional[float] = None,
        ttl: Optional[int] = None,
        create: bool = True,
        display_name: Optional[str] = None,
    ) -> CheckResult | CheckError:
        """
        Send a check result for a service and create the host or the service if necessary.

        :param service: The name of the service.
        :param host: The name of the host.
        :param exit_status: For services: ``0=OK``, ``1=WARNING``, ``2=CRITICAL``,
            ``3=UNKNOWN``, for hosts: ``0=UP``, ``1=DOWN``.
        :param plugin_output: One or more lines of the plugin main output. Does **not**
            contain the performance data.
        :param performance_data: The performance data.
        :param check_command: The first entry should be the check commands path, then
            one entry for each command line option followed by an entry for each of its
            argument. Alternativly a single string can be used.
        :param check_source: Usually the name of the ``command_endpoint``.
        :param execution_start: The timestamp where a script/process started its
            execution.
        :param execution_end: The timestamp where a script/process ended its execution.
            This timestamp is used in features to determine e.g. the metric timestamp.
        :param ttl: Time-to-live duration in seconds for this check result. The next
            expected check result is ``now + ttl`` where freshness checks are executed.
        :param create: Whether non-existent services and hosts should be created.
        :param display_name: A short description of the service, if it needs to be created.
        """
        host = _get_host(host)

        if exit_status is None:
            exit_status = ServiceState.OK

        if plugin_output is None:
            plugin_output = f"{service}: {exit_status}"

        def _send_service_check_result() -> CheckResult | CheckError:
            name = f"{host}!{service}"
            logger.info(
                "Send service check result: %s exit_status: %s plugin_output: %s",
                name,
                exit_status,
                plugin_output,
            )
            result = self.raw_client.actions.process_check_result(
                type="Service",
                name=f"{host}!{service}",
                exit_status=exit_status,
                plugin_output=plugin_output,
                performance_data=performance_data,
                check_command=check_command,
                check_source=check_source,
                execution_start=execution_start,
                execution_end=execution_end,
                ttl=ttl,
                suppress_exception=True,
            )
            if "results" in result and len(result["results"]) > 0:
                return CheckResult(**result["results"][0])
            return CheckError(**result)

        result: CheckResult | CheckError = _send_service_check_result()

        if isinstance(result, CheckResult):
            return result

        if not create:
            return result

        self.create_host(
            name=host,
            object_config=self.config.new_host_defaults,
            suppress_exception=True,
        )
        self.create_service(
            name=service,
            host=host,
            object_config=self.config.new_host_defaults,
            suppress_exception=True,
            display_name=display_name,
        )

        return _send_service_check_result()

    # time_period ######################################################################

    def get_time_periods(self) -> Sequence[TimePeriod]:
        return self._get_objects(TimePeriod)

    # user #############################################################################

    def get_users(self) -> Sequence[User]:
        return self._get_objects(User)

    # status ###########################################################################

    def get_status(self) -> Sequence[StatusMessage]:
        result = self.raw_client.status.list()
        adapter = TypeAdapter(
            list[StatusMessage], config={"arbitrary_types_allowed": True}
        )
        return adapter.validate_python(result["results"])
