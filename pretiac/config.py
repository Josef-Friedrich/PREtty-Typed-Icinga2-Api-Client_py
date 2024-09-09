import os
from pathlib import Path
from typing import Literal, Optional, Sequence, Union

import yaml
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from pretiac.exceptions import PretiacException
from pretiac.object_types import Payload


@dataclass(config={"extra": "forbid"})
class ObjectConfig:
    """
    Bundles all configuration required to create an object.
    """

    templates: Optional[Sequence[str]] = None
    """
    Import existing configuration templates for this
    object type. Note: These templates must either be statically
    configured or provided in config packages.
    """

    attrs: Optional["Payload"] = None
    """Set specific object attributes for this object type."""


@dataclass(config={"extra": "forbid"})
class Config:
    """
    :see: `pretiac (JS) <https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_js/blob/722c6308d79f603a9ad7678609cd907b932c64ab/src/client.ts#L7-L15>`__
    """

    config_file: Optional[Path] = None
    """The path of the loaded configuration file."""

    api_endpoint_host: Optional[str] = None
    """
    The domain or the IP address of the API endpoint, e. g. ``icinga.example.com``,
    ``localhost`` or ``127.0.0.1``.
    """

    api_endpoint_port: Optional[int] = None
    """The TCP port of the API endpoint, for example ``5665``.

    :see: `Icinca Object Types (apilistener) <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener>`__
    """

    http_basic_username: Optional[str] = None
    """
    The name of the API user used in the HTTP basic authentification, e. g. ``apiuser``.

    .. code-block ::

        object ApiUser "apiuser" {
            ...
        }

    :see: `Icinca Object Types (apiuser) <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser>`__
    """

    http_basic_password: Optional[str] = None
    """
    The password of the API user used in the HTTP basic authentification, e. g. ``password``.

    .. code-block ::

        object ApiUser "apiuser" {
            password = "password"
        }

    :see: `Icinca Object Types <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser>`__
    """

    client_private_key: Optional[str] = None
    """
    The file path of the client’s **private RSA key**, for example
    ``/etc/pretiac/api-client.key.pem``.

    The RSA private key is created with this command:

    .. code-block ::

        icinga2 pki new-cert \\
            --cn api-client \\
            --key api-client.key.pem \\
            --csr api-client.csr.pem
    """

    client_certificate: Optional[str] = None
    """
    The file path of the client **certificate**.

    The certificate is created with this command:

    .. code-block ::

        icinga2 pki sign-csr \\
            --csr api-client.csr.pem \\
            --cert api-client.cert.pem
    """

    ca_certificate: Optional[str] = None
    """
    The file path of the Icinga **CA (Certification Authority)**.

    The CA certificate is located at ``/var/lib/icinga2/certs/ca.crt``. This
    command copies the certificate to the local host.

    .. code-block ::

        scp icinga-master:/var/lib/icinga2/certs/ca.crt .
    """

    suppress_exception: Optional[bool] = None
    """
    If set to ``True``, no exceptions are thrown.
    """

    new_host_defaults: Optional[ObjectConfig] = None
    """If a new host needs to be created, use this defaults."""

    new_service_defaults: Optional[ObjectConfig] = None
    """If a new service needs to be created, use this defaults."""

    def check(self) -> None:
        """Check if all required values are set."""
        if self.api_endpoint_host is None:
            raise PretiacException("Specify an API endpoint host (api_endpoint_host)!")

        if (self.http_basic_username or self.http_basic_password) and (
            self.client_private_key or self.client_certificate or self.ca_certificate
        ):
            raise PretiacException(
                "Specify HTTP basic OR certificate authentification. Not both!"
            )


def load_config_file(config_file: Optional[Union[str, Path]] = None) -> Config:
    """
    Load the configuration file in YAML format.

    The file path of the loaded configuration file is determined in this order:

    1. The parameter ``config_file`` of this function.
    2. The file path in the environment variable ``PRETIAC_CONFIG_FILE``.
    3. The configuration file in the home folder ``~/.pretiac.yml``.
    4. The configuration file at ``/etc/pretiac/config.yml``.

    :param config_file: The path of the configuration file to load.
    """
    config_files: list[Path] = []
    if config_file:
        if isinstance(config_file, str):
            config_files.append(Path(config_file))
        else:
            config_files.append(config_file)
    if "PRETIAC_CONFIG_FILE" in os.environ:
        config_files.append(Path(os.environ["PRETIAC_CONFIG_FILE"]))
    config_files.append(Path.cwd() / ".pretiac.yml")
    config_files.append(Path("/etc/pretiac/config.yml"))

    for path in config_files:
        if path.exists():
            config_file = path
            break

    adapter = TypeAdapter(Config)

    if not config_file:
        return adapter.validate_python({})

    with open(config_file, "r") as file:
        config_raw = yaml.safe_load(file)
        config_raw["config_file"] = str(config_file)
    return adapter.validate_python(config_raw)


def load_config(
    config: Optional[Config] = None,
    config_file: Optional[Union[str, Path, Literal[False]]] = None,
    api_endpoint_host: Optional[str] = None,
    api_endpoint_port: Optional[int] = None,
    http_basic_username: Optional[str] = None,
    http_basic_password: Optional[str] = None,
    client_private_key: Optional[str] = None,
    client_certificate: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    suppress_exception: Optional[bool] = None,
    new_host_defaults: Optional[ObjectConfig] = None,
    new_service_defaults: Optional[ObjectConfig] = None,
) -> Config:
    """
    :param config: A configuration object that has already been populated.
    :param config_file: The path of the configuration file to load.
        If this value is set to false no configuration file will be loaded.
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
    :param new_host_defaults: If a new host needs to be created, use this
        defaults.
    :param new_service_defaults: If a new service needs to be created, use
        this defaults.
    """
    if config is not None and (config_file is not None and config_file is not False):
        raise PretiacException("Specify config OR config_file. Not both!")

    c: Optional[Config] = None
    if config:
        c = config
    elif config_file is False:
        c = Config()
    else:
        c = load_config_file(config_file)

    if api_endpoint_host is not None:
        c.api_endpoint_host = api_endpoint_host

    if api_endpoint_port is not None:
        c.api_endpoint_port = api_endpoint_port

    if c.api_endpoint_port is None:
        c.api_endpoint_port = 5665

    if http_basic_username is not None:
        c.http_basic_username = http_basic_username

    if http_basic_password is not None:
        c.http_basic_password = http_basic_password

    if client_private_key is not None:
        c.client_private_key = client_private_key

    if client_certificate is not None:
        c.client_certificate = client_certificate

    if ca_certificate is not None:
        c.ca_certificate = ca_certificate

    if suppress_exception is not None:
        c.suppress_exception = suppress_exception

    if new_host_defaults is not None:
        c.new_host_defaults = new_host_defaults

    if new_service_defaults is not None:
        c.new_service_defaults = new_service_defaults

    c.check()

    return c
