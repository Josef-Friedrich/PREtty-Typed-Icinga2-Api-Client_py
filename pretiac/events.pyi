from collections.abc import Generator

from _typeshed import Incomplete

from .base import Base as Base

LOG: Incomplete

class Events(Base):
    base_url_path: str
    def subscribe(
        self,
        types,
        queue,
        filters: Incomplete | None = ...,
        filter_vars: Incomplete | None = ...,
    ) -> Generator[Incomplete, None, None]: ...
