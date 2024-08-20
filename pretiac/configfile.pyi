from _typeshed import Incomplete

from pretiac.exceptions import (
    Icinga2ApiConfigFileException as Icinga2ApiConfigFileException,
)

class ClientConfigFile:
    file_name: Incomplete
    section: str
    url: Incomplete
    username: Incomplete
    password: Incomplete
    certificate: Incomplete
    key: Incomplete
    ca_certificate: Incomplete
    timeout: Incomplete
    def __init__(self, file_name) -> None: ...
    def check_access(self): ...
    def parse(self) -> None: ...
