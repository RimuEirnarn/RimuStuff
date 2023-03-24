"""Database"""
from atexit import register as atexit_register
from sqlite3 import OperationalError, connect
from typing import Iterable, Optional

from ._utils import (WithCursor, check_iter, check_one, dict_factory, null,
                     sqlite_multithread_check, AttrDict)
from .column import BuilderColumn, Column
from .locals import this
from .query_builder import extract_table_creations
from .signature import op
from .table import Table
Columns = Iterable[Column] | Iterable[BuilderColumn]


class Database:
    """Sqlite3 database, this provide basic integration."""

    _active: dict[str, "Database"] = {}

    def __new__(cls, path: str, **kwargs):
        if path in cls._active:
            return cls._active[path]
        self = object.__new__(cls)
        self.__init__(path, **kwargs)
        if path != ":memory:":
            cls._active[path] = self
        return self

    def __init__(self, path: str, **kwargs) -> None:
        kwargs['check_same_thread'] = sqlite_multithread_check() != 3
        self._path = path
        self._database = connect(path, **kwargs)
        self._database.row_factory = dict_factory
        self._closed = False
        self._table_instances: dict[str, Table] = {}
        # pylint: disable-next=unnecessary-lambda
        atexit_register(lambda: self.close())  # type: ignore

    def cursor(self) -> WithCursor:
        """Create cursor"""
        return self._database.cursor(WithCursor)  # type: ignore

    def create_table(self, table: str, columns: Columns):
        """Create table

        Args:
            table (str): Table name
            columns (Iterable[Column]): Columns for table

        Returns:
            Table: Newly created table
        """
        check_one(table)
        columns = (column.to_column() if isinstance(
            column, BuilderColumn) else column for column in columns)
        tbquery = extract_table_creations(columns)
        query = f"create table {table} ({tbquery})"

        with self._database as that:
            that.execute(query)
        table_ = self.table(table, columns)
        table_._deleted = False  # pylint: disable=protected-access
        self._table_instances[table] = table_
        return table_

    def delete_table(self, table: str):
        """Delete an existing table

        Args:
            table (str): table name
        """
        check_one(table)
        table_ = self.table(table)
        with self._database as that:
            that.execute(f"drop table {table}")
        # pylint: disable-next=protected-access
        del self._table_instances[table]
        table_._delete_hook()  # pylint: disable=protected-access

    def table(self, table: str, __columns: Optional[Iterable[Column]] = None):
        """fetch table"""
        if self._table_instances.get(table, None) is not None:
            return self._table_instances[table]
        this_table = Table(self, table, __columns)
        self._table_instances[table] = this_table
        return this_table

    def reset_table(self, table: str, columns: Columns) -> Table:
        """Reset existing table with new, this rewrote entire table than altering it."""
        try:
            self.table(table)
            self.delete_table(table)
        except OperationalError:
            pass
        return self.create_table(table, columns)

    def rename_table(self, old_table: str, new_table: str) -> Table:
        """Rename existing table to a new one."""
        check_iter((old_table, new_table))
        self.sql.execute(f"alter table {old_table} rename to {new_table}")
        self.sql.commit()
        return self.table(new_table)

    def __repr__(self) -> str:
        return f"<Database {id(self)}>"

    def close(self):
        """Close database"""
        self._database.close()
        self._closed = True

    @property
    def closed(self):
        """Is database closed?"""
        return self._closed

    @closed.setter
    def closed(self, __o: bool):
        """Is database closed?"""
        if __o:
            self.close()
            return
        raise ValueError("Expected non-false/non-null value")

    @property
    def path(self):
        """Path to SQL Connection"""
        return "Memory" or self._path

    @property
    def sql(self):
        """SQL Connection"""
        return self._database


__all__ = ["Database", "Table", "this", "op", "WithCursor",
           "Column", "null", 'AttrDict']
