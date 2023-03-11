"""Bootstrap"""
from warnings import warn

from flask import Flask
try:
    from app.utils import save_exc_groups
    from core.typings import BootstrapFunction
except ImportError:
    from .utils import save_exc_groups
    from ..core.typings import BootstrapFunction


_PENDING_BOOTSTRAP: list[BootstrapFunction] = []

SETTINGS = {
    'keep': True,
    'true_keep': False
}


def register(func: BootstrapFunction):
    """Register a function to bootstrapping list"""
    _PENDING_BOOTSTRAP.append(func)


def remove(func: BootstrapFunction):
    """Remove a function from bootstraping list"""
    try:
        _PENDING_BOOTSTRAP.remove(func)
    except ValueError:
        raise ValueError("No such callable.") from None


def bootstrap(app: Flask):
    """Initialize or run all bootstrap function."""
    errors: list[BaseException] = []
    for calls in _PENDING_BOOTSTRAP:
        try:
            if calls is bootstrap:
                raise ValueError(
                    "An illegal function has been passed to bootstrap list.")
            calls(app)
        except Exception as exc:
            if SETTINGS.get('keep', False):
                errors.append(exc)
                continue
            raise

    if errors:
        try:
            raise ExceptionGroup("Bootrapping failed!", errors)  # type: ignore
        except ExceptionGroup as main_exc:
            if SETTINGS.get("true_keep", False):
                raise
            warn("Some errors have been occured. It is saved to bootstrap-reports.txt")
            save_exc_groups("bootstrap-reports.txt", main_exc)
