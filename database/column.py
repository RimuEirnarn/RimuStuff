"""Column"""

from typing import Any
from .locals import _PATH, SQLACTION, SQLITETYPES
from ._utils import check_one, matches


class Column:  # pylint: disable=too-many-instance-attributes
    """Column

    tip: for foreign_ref, you can split with / to separate table and column name.
    e.g: user/id"""

    def __init__(self,  # pylint: disable=too-many-arguments
                 name: str,
                 type_: SQLITETYPES,
                 foreign: bool = False,
                 foreign_ref: str | None = None,
                 primary: bool = False,
                 unique: bool = False,
                 nullable: bool = True,
                 default: Any = None,
                 on_delete: SQLACTION = "cascade",
                 on_update:
                 SQLACTION = "cascade") -> None:
        self._name = check_one(name)
        self._type = check_one(type_)
        self._unique = unique
        self._nullable = nullable
        self._default = default
        self._foreign_enabled = foreign
        while foreign_ref:
            if not matches(_PATH, foreign_ref):
                raise ValueError(
                    "foreign_ref has no / separator to separate table and column.")
            ref = foreign_ref.split('/', 1)
            source = ref[0]
            scolumn = ref[1] if len(ref) == 2 else name
            self._source = source
            self._source_column = scolumn
            self._foreign = foreign_ref
            break

        if not foreign:
            self._foreign = None
            self._foreign_enabled = False
        self._update = on_update
        self._delete = on_delete
        self._is_primary = primary

    @property
    def name(self):
        """Column Name"""
        return self._name

    @property
    def unique(self):
        """Is unique"""
        return self._unique

    @property
    def default(self):
        """Default value"""
        return self._default

    @property
    def nullable(self):
        """Nullable"""
        return self._nullable

    @property
    def raw_source(self):
        """Source / Foreign Reference"""
        return self._foreign

    @property
    def foreign(self):
        """Is foreign enabled?"""
        return self._foreign_enabled

    @property
    def source(self):
        """Source / Foreign Reference"""
        if self._foreign is None:
            raise AttributeError("Source is unset")
        return self._source

    @property
    def source_column(self):
        """Source column / Foreign reference column"""
        if self._foreign is None:
            raise AttributeError("Source column is unset")
        return self._source_column

    @property
    def primary(self):
        """Is primary or not?"""
        return self._is_primary

    @property
    def on_update(self):
        """Update setting"""
        return self._update

    @property
    def on_delete(self):
        """Delete setting"""
        return self._delete

    @property
    def type(self):
        """Type"""
        return self._type

    def __repr__(self) -> str:
        return f"<{self.type.title()}{type(self).__name__} -> {self.name}>"

    def __eq__(self, __o: 'Column') -> bool:
        if not isinstance(__o, Column):
            raise NotImplementedError
        other = (__o.name, __o.type, __o.unique, __o.nullable, __o.default,
                 __o.primary, __o.raw_source, __o.on_delete, __o.on_update)
        self_ = (self.name, self.type, self.unique, self.nullable, self.default,
                 self.primary, self.raw_source, self.on_delete, self.on_update)
        return all((item1 in self_ for item1 in other))
