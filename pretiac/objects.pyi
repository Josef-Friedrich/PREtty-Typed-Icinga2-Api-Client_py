from typing import List, Union

from _typeshed import Incomplete as Incomplete

from pretiac.base import Base, Json, ObjectType

LOG: Incomplete

class Objects(Base):
    base_url_path: str
    def get(
        self,
        object_type: ObjectType,
        name: str,
        attrs: Union[Incomplete, None] = ...,
        joins: Union[Incomplete, None] = ...,
    ) -> Json: ...
    def list(
        self,
        object_type: ObjectType,
        name: str | None = ...,
        attrs: List[str] | None = ...,
        filters: str | None = ...,
        filter_vars: Union[Incomplete, None] = ...,
        joins: bool | List[str] | None = ...,
    ) -> Json: ...
    def create(
        self,
        object_type: ObjectType,
        name: str,
        templates: Union[Incomplete, None] = ...,
        attrs: Union[Incomplete, None] = ...,
    ) -> Json: ...
    def update(self, object_type: ObjectType, name: str, attrs) -> Json: ...
    def delete(
        self,
        object_type: ObjectType,
        name: Union[Incomplete, None] = ...,
        filters: Union[Incomplete, None] = ...,
        filter_vars: Union[Incomplete, None] = ...,
        cascade: bool = ...,
    ) -> Json: ...
