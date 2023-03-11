"""Database Loader"""
try:
    from ..database import Database
except ImportError:
    from database import Database

database = Database("main.db")


def table_namespace(table_name: str):
    """Return namespace for table"""
    return database.table(table_name).get_namespace()


def table(table_name: str):
    """Return table of a database"""
    return database.table(table_name)
