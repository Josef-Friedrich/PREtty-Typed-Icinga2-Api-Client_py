from logging import Logger

from icinga2apic.objects import Objects

from .actions import Actions

LOG: Logger = ...

class Client:

    actions: Actions

    objects: Objects

    def __init__(
        self,
        url: str | None = ...,
        username: str | None = ...,
        password: str | None = ...,
        timeout: int | None = ...,
        certificates: str | None = ...,
        key: str | None = ...,
        ca_certificate: str | None = ...,
        config_file: str | None = ...,
    ) -> None: ...
