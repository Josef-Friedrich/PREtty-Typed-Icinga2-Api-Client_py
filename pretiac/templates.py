"""
Provides methods to querying configuration templates:

Creation, modification and deletion of templates at runtime is not supported.

https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#config-templates
"""

from typing import Any, Optional

from pretiac.base import Base, ObjectTypeName, Payload


class Templates(Base):
    base_url_path = "v1/templates"

    def list(self, object_type: ObjectTypeName, filter: Optional[str] = None) -> Any:
        """Request information about configuration templates.

        :param object_type: The type of the object, for example ``Service``,
            ``Host`` or ``User``.
        :param filter: The template object can be accessed in the filter using the
            ``tmpl`` variable. In the example ``"match(\"g*\", tmpl.name)"``
            the match function is used to check a wildcard string pattern against
            ``tmpl.name``.
        """
        payload: Payload = {}
        if filter:
            payload["filter"] = filter
        return self._request(
            "GET", f"{self.base_url}/{self._pluralize(object_type)}", payload
        )
