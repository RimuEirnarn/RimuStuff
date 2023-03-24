"""Collections of Proxy"""

from typing import Any

from sqlite_database._utils import AttrDict

_null = object()


class ProxyAttrDict:
    """Proxy AttrDict"""

    def __init__(self, obj: AttrDict) -> None:
        self._instance = obj

    def __getattr__(self, __name: str):
        return getattr(self._instance, __name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        self._instance[__name] = __value

    def __getitem__(self, __key: str) -> Any:
        return self._instance[__key]

    def __setitem__(self, __key: str, __value: Any):
        self._instance[__key] = __value
