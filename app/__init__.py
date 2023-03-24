"""Application"""
from flask import Flask
from flask_login import LoginManager, current_user
from sqlite_database import op

from .model.user import UserInterface
from .skeleton.user import UserSkeleton

from .flask_utils import get_admin, get_moderator
from .utils import load as toml_load
from .database_loader import database


try:
    from ..core.router import Router
except ImportError:
    from core.router import Router

login_manager = LoginManager()

Route = Router()


def register_user_model(app: Flask, model: UserSkeleton):
    """Register user model"""
    login_manager.user_loader(model.get)
    login_manager.init_app(app)


def register_login(base: Flask):
    """This function should be registered in `bootstrap.register`"""
    register_user_model(base, UserInterface)  # type: ignore


def create_app():
    """Bootstrap app creation"""
    base = Flask(__name__)
    base.config.from_file("../config.toml", toml_load)  # type: ignore

    groups = database.table('groups')
    _rootgroup = groups.select_one({"gid": op == 0})
    _psadmin = groups.select_one({"gid": op == 999})
    rootgroup = _rootgroup['name'] if _rootgroup else get_admin()
    pseudo_admin = _psadmin['name'] if _psadmin else get_moderator()

    @base.template_global()
    def is_admin():
        """Is user admin"""
        if current_user is None:
            return False
        uroles: list[str] = current_user.groups.split(',')  # type: ignore
        if rootgroup in uroles:
            return True
        return False

    @base.template_global()
    def is_moderator():
        """Is user moderator"""
        if current_user is None:
            return False
        uroles: list[str] = current_user.groups.split(',')  # type: ignore
        if pseudo_admin in uroles:
            return True
        return False

    return base
