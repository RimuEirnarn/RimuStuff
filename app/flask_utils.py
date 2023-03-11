"""Flask utils"""
from functools import partial, wraps
from re import compile as re_compile
from re import escape as re_escape
from string import punctuation
from types import SimpleNamespace
from typing import Any

from flask import Response, abort
from flask_login import current_user

try:
    from app.utils import has_common_item
except ImportError:
    from .utils import has_common_item

_USERNAMEPASS_STR = punctuation.replace("_", "").replace('.', "")
_USERNAME = re_compile(f"[{re_escape(_USERNAMEPASS_STR)}]+")
_NameSpace = SimpleNamespace(admin='root')


def set_admin(role_name: str):
    """Set admin role (this used for role_required for admins to bypass role restrictions)"""
    _NameSpace.admin = role_name


def set_moderator(role_name: str):
    """Set moderator role (this used for role_required for admins to bypass role restrictions)"""
    _NameSpace.mod = role_name


def get_admin() -> str:
    """Get admin role"""
    return getattr(_NameSpace, "admin", "root")


def get_moderator() -> str:
    """Get admin role"""
    return getattr(_NameSpace, "mod", "root")


def role_required(*roles: str, code=403):
    """Add role filter to view/function.

    Put role names, and they should be done.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Response | str:
            if current_user is None:
                return abort(code)
            # if user is admin, we should always return func()
            user_roles: list[str] = current_user.groups.split(
                ',')  # type: ignore
            if get_admin() in user_roles:
                return func(*args, **kwargs)
            if not has_common_item(roles, user_roles):
                return abort(code)
            return func(*args, **kwargs)
        return wrapper
    return decorator


admin_only = partial(role_required, "admin")


def is_invalid_username(username: str) -> bool:
    """Is username is invalid?

    Args:
        username (str): Username

    Returns:
        bool: True if invalid
    """
    if _USERNAME.findall(username):
        return True
    return False
