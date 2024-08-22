import json
import os
from pathlib import Path

from pydantic import BaseModel, Field

from pretiac.exceptions import PretiacConfigFileException


class Config(BaseModel):
    """
    https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_js/blob/722c6308d79f603a9ad7678609cd907b932c64ab/src/client.ts#L7-L15
    """

    domain: str
    """
    The domain, e. g. ``icinga.example.com`` or ``localhost``.
    """

    port: int = 5665
    """The TCP port, by default ``5665``

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener
    """

    api_user: str = Field(alias="apiUser")
    """
    The name of the API user, e. g. ``apiuser``.

    .. code-block ::

        object ApiUser "apiuser" {
            ...
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser
    """

    password: str
    """
    The password of the API user, e. g. ``password``.

    .. code-block ::

        object ApiUser "apiuser" {
            password = "password"
        }

    https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apiuser
    """


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
        raise PretiacConfigFileException("The configuration file could not be found.")

    with open(config_file, "r") as stream:
        config_raw = json.load(stream)
    return Config(**config_raw)
