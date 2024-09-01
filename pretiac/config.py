import json
import os
from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel, Field

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

    api_endpoint_host: Optional[str] = Field(alias="apiEndpointHost", default=None)
    """
    The domain or the IP address of the API endpoint, e. g. ``icinga.example.com``
    or ``localhost``.
    """

    api_endpoint_port: Optional[int] = Field(alias="apiEndpointPort", default=None)
    """The TCP port of the API endpoint, for example ``5665``.

    :see: `Icinca Object Types (apilistener) <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener>`__
    """

    http_basic_username: Optional[str] = Field(alias="httpBasicUsername", default=None)
    """
    The name of the API user used in the HTTP basic authentification, e. g. ``apiuser``.

    .. code-block ::

        object ApiUser "apiuser" {
            ...
        }

    :see: `Icinca Object Types (apiuser) <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser>`__
    """

    http_basic_password: Optional[str] = Field(alias="httpBasicPassword", default=None)
    """
    The password of the API user used in the HTTP basic authentification, e. g. ``password``.

    .. code-block ::

        object ApiUser "apiuser" {
            password = "password"
        }

    :see: `Icinca Object Types <https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser>`__
    """

    client_private_key: Optional[str] = Field(alias="clientPrivateKey", default=None)
    """
    The file path of the client **RSA private key**.

    The RSA private key is created with this command:

    .. code-block ::

        icinga2 pki new-cert \\
            --cn api-client \\
            --key api-client.key.pem \\
            --csr api-client.csr.pem
    """

    client_certificate: Optional[str] = Field(alias="clientCertificate", default=None)
    """
    The file path of the client **certificate**.

    The certificate is created with this command:

    .. code-block ::

        icinga2 pki sign-csr \\
            --csr api-client.csr.pem \\
            --cert api-client.cert.pem
    """

    ca_certificate: Optional[str] = Field(alias="caCertificate", default=None)
    """
    The file path of the Icinga **CA (Certification Authority)**.

    The CA certificate is located at ``/var/lib/icinga2/certs/ca.crt``. This
    command copies the certificate to the local host.

    .. code-block ::

        scp icinga-master:/var/lib/icinga2/certs/ca.crt .
    """

    suppress_exception: Optional[bool] = Field(alias="suppressException", default=None)
    """
    If set to ``True``, no exceptions are thrown.
    """

    new_host_defaults: Optional[ObjectConfig] = Field(
        alias="newHostDefaults", default=None
    )
    """If a new host needs to be created, use this defaults."""

    new_service_defaults: Optional[ObjectConfig] = Field(
        alias="newServiceDefaults", default=None
    )
    """If a new service needs to be created, use this defaults."""

    config_file: Optional[Path] = Field(alias="configFile", default=None)
    """The path of the loaded configuration file."""


def load_config(config_file: str | Path | None = None) -> Config:
    """
    Load the configuration file in JSON format.

    1. Parameter ``config_file`` of the function.
    2. Enviroment variable ``ICINGA_API_CLIENT``.
    3. Configuration file in the home folder ``~/.icinga-api-client.json``.
    4. Configuration file in ``/etc/icinga-api-client/config.json``.
    """
    config_files: list[Path] = []
    if config_file:
        if isinstance(config_file, str):
            config_files.append(Path(config_file))
        else:
            config_files.append(config_file)
    if "ICINGA_API_CLIENT" in os.environ:
        config_files.append(Path(os.environ["ICINGA_API_CLIENT"]))
    config_files.append(Path.cwd() / ".icinga-api-client.json")
    config_files.append(Path("/etc/icinga-api-client/config.json"))

    for path in config_files:
        if path.exists():
            config_file = path
            break

    if not config_file:
        return Config()

    with open(config_file, "r") as stream:
        config_raw = json.load(stream)
        config_raw["configFile"] = str(config_file)
    return Config(**config_raw)
