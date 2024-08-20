from _typeshed import Incomplete

from .base import Base as Base

LOG: Incomplete

class Status(Base):
    base_url_path: str
    def list(self, component: Incomplete | None = ...): ...
