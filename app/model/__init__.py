"""Models"""

from inspect import get_annotations
from typing import Protocol

from sqlite_database.table import Table
from sqlite_database.typings import TypicalNamedTuple


try:
    from ...core.proxies import AttrDict
except ImportError:
    from core.proxies import AttrDict

class AnyModel(Protocol):
    """Model Protocol"""
    _table: 'Table'  # type: ignore
    _raw_attributes: TypicalNamedTuple
    _attrs: AttrDict

    @staticmethod
    def find(user_id: str):
        """Find and fetch from user_id"""

    @staticmethod
    def all():
        """Find all data from resoruce"""

    def save(self):
        """Save upheld data to database"""

    def destroy(self):
        """Delete current data from database"""

    def __repr__(self) -> str:
        return f"{type(self).__name__}({id(self)})"


class BaseModel(AnyModel):
    """Base Models"""
    _table: Table

    def __init_subclass__(cls, table: Table):  # pylint: disable=arguments-differ
        cls._table = table
        namespace = table.get_namespace()
        for varname, annotated in get_annotations(namespace).items():
            def temp_function(varname):
                def wrapper(self: BaseModel):
                    return getattr(self._attrs, varname)  # pylint: disable=protected-access
                return wrapper
            tmp_fn = temp_function(varname)
            tmp_fn.__name__ = varname
            tmp_fn.__qualname__ = varname
            tmp_fn.__annotations__['return'] = annotated
            cls.__annotations__[varname] = annotated
            setattr(cls, varname, property(tmp_fn))

    def __init__(self, _query: AttrDict) -> None:
        super().__init__()
        self._raw_attributes = self._table.get_namespace()(**_query)
        self._attrs = _query

    @staticmethod
    def find(user_id: str):
        return

    @staticmethod
    def all():
        pass

    def save(self):
        self._table.update_one(self._attrs, self._raw_attributes._asdict())

    def destroy(self):
        self._table.delete_one(self._raw_attributes._asdict())
