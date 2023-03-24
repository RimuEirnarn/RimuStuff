"""app"""
# pylint: disable=all
from functools import wraps
from html import escape

from flask import Flask, abort, flash, redirect, render_template, request, url_for, g
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, \
    logout_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from sqlite_database import Database, op

try:
    from app.flask_utils import get_admin, get_moderator, is_invalid_username, role_required, admin_only
    from app.utils import load as toml_load
    from app.utils import usage_cache
except ImportError:
    from .flask_utils import get_admin, get_moderator, is_invalid_username, \
        role_required, admin_only
    from .utils import load as toml_load
    from .utils import usage_cache


# data


@usage_cache(10)
def _read():
    with open("templates/_navbar.html", encoding='utf-8') as file:
        return file.read()


def _pre_render(*args, **kwargs):
    kwargs['navbar'] = _read()
    return render_template(*args, **kwargs)


app = Flask(__name__)
app.config.from_file("config.toml", toml_load)  # type: ignore

database = Database("main.db")
users = database.table("users")
groups = database.table('groups')
pre_render = wraps(render_template)(_pre_render)
_rootgroup = groups.select_one({"gid": op == 0})
_psadmin = groups.select_one({"gid": op == 999})
rootgroup = _rootgroup['name'] if _rootgroup else get_admin()
pseudo_admin = _psadmin['name'] if _psadmin else get_moderator()
with app.app_context():
    g.admin = rootgroup
    g.psadmin = pseudo_admin
# Internal


loginmanager = LoginManager()
loginmanager.init_app(app)
