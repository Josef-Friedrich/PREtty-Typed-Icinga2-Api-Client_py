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
    https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_js/blob/722c6308d79f603a9ad7678609cd907b932c64ab/src/client.ts#L7-L15
    """

    domain: Optional[str] = None
    """
    The domain, e. g. ``icinga.example.com`` or ``localhost``.
    """

    port: Optional[int] = None
    """The TCP port`

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener
    """

    api_user: Optional[str] = Field(alias="apiUser", default=None)
    """
    The name of the API user, e. g. ``apiuser``.

    .. code-block ::

        object ApiUser "apiuser" {
            ...
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser
    """

    password: Optional[str] = None
    """
    The password of the API user, e. g. ``password``.

    .. code-block ::

        object ApiUser "apiuser" {
            password = "password"
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser
    """

    certificate: Optional[str] = None

    key: Optional[str] = None

    ca_certificate: Optional[str] = None

    suppress_exception: Optional[bool] = None
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
    return Config(**config_raw)
