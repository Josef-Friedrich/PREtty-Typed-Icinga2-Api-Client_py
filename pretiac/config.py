import os
from pathlib import Path
from typing import Optional, Sequence

import yaml
from pydantic import BaseModel

from pretiac.exceptions import PretiacException
from pretiac.object_types import Payload


class ObjectConfig(BaseModel):
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


class Config(BaseModel):
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


def load_config_file(config_file: str | Path | None = None) -> Config:
    """
    Load the configuration file in JSON format.

    1. Parameter ``config_file`` of the function.
    2. Enviroment variable ``PRETIAC_CONFIG_FILE``.
    3. Configuration file in the home folder ``~/.pretiac.yml``.
    4. Configuration file in ``/etc/pretiac/config.yml``.

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

    if not config_file:
        return Config()

    with open(config_file, "r") as file:
        config_raw = yaml.safe_load(file)
        config_raw["config_file"] = str(config_file)
    return Config(**config_raw)


def load_config(
    config_file: Optional[str | Path] = None,
    api_endpoint_host: Optional[str] = None,
    api_endpoint_port: Optional[int] = None,
    http_basic_username: Optional[str] = None,
    http_basic_password: Optional[str] = None,
    client_private_key: Optional[str] = None,
    client_certificate: Optional[str] = None,
    ca_certificate: Optional[str] = None,
    suppress_exception: Optional[bool] = None,
) -> Config:
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
    config: Config = load_config_file(config_file)

    if api_endpoint_host is not None:
        config.api_endpoint_host = api_endpoint_host

    if config.api_endpoint_host is None:
        raise PretiacException("no domain")

    if api_endpoint_port is not None:
        config.api_endpoint_port = api_endpoint_port

    if config.api_endpoint_port is None:
        config.api_endpoint_port = 5665

    if http_basic_username is not None:
        config.http_basic_username = http_basic_username

    if http_basic_password is not None:
        config.http_basic_password = http_basic_password

    if client_private_key is not None:
        config.client_private_key = client_private_key

    if client_certificate is not None:
        config.client_certificate = client_certificate

    if ca_certificate is not None:
        config.ca_certificate = ca_certificate

    if suppress_exception is not None:
        config.suppress_exception = suppress_exception

    return config
