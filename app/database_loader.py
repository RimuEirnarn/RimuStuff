"""Database Loader"""
from sqlite_database import Database

database = Database("main.db")


def table_namespace(table_name: str):
    """Return namespace for table"""
    return database.table(table_name).get_namespace()  # type: ignore


def table(table_name: str):
    """Return table of a database"""
    return database.table(table_name)
