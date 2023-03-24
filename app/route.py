"""Main Route"""
# pylint: disable=missing-function-docstring,missing-class-docstring
from flask_login import login_required, login_user, logout_user
from flask import render_template, request, flash, redirect, url_for, abort
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash
from sqlite_database.signature import op


try:
    from app import Route
    from app.forms import LoginForm, RegisterForm
    from app.database_loader import table
    from app.model.user import UserInterface
    from app.flask_utils import is_invalid_username, role_required, admin_only
except ImportError:
    from . import Route
    from .forms import LoginForm, RegisterForm
    from .model.user import UserInterface
    from .flask_utils import is_invalid_username, role_required, admin_only
    from .database_loader import table

users = table('users')
groups = table('groups')


@login_required
@Route.get("/")
def root():
    return render_template("root.html")


@Route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", form=LoginForm())
    loginform = LoginForm()
    if not loginform.validate_on_submit():
        return render_template("login.html", form=loginform)
    username: str = loginform.username.data
    passwd: str = loginform.password.data
    user = users.select_one({"username": op == username})
    if user is None:
        flash(f"{escape(username)} is not exist.", 'error')
        return render_template("login.html", form=loginform)

    if not check_password_hash(user.password, passwd):
        flash("Invalid password.", "error")
        return render_template("login.html", form=loginform)
    login_user(UserInterface.get(user.username), True)
    flash('Logged in successfully.', 'success')
    return redirect("/")


@Route.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", form=RegisterForm())
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template("register.html", form=form)
    username, password = form.username.data, form.password.data
    if users.exists({"username": op == username}):
        flash("This username is already exists.", 'error')
        return render_template("register.html", form=form)
    if is_invalid_username(username):
        flash("Username can only have . and/or _ special characters.", 'error')
        return render_template("register.html", form=form)
    users.insert(
        {"username": username, "password": generate_password_hash(password)})
    flash('Registered successfully. Please login.', 'success')
    return redirect(url_for('login'))


@Route.post('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('root'))


@Route.get("/settings")
@login_required
def settings():
    return render_template("settings.html")


@Route.get("/internal")
@role_required("admin", code=404)
def internal():
    return render_template("internal.html")


@Route.get("/internal/settings")
@role_required("admin", code=404)
def internal_settings():
    return render_template("serversettings.html")


@Route.get("/abort/<int:code>")
@role_required("admin", code=404)
def abort_(code: int):
    return abort(code)


@Route.get("/files/<path:filepath>")
@role_required("admin", code=403)
def files_index(filepath):
    return f"/{filepath}"


@Route.get("/files")
@Route.get("/files/")
@role_required("admin", code=403)
def files_root():
    return "/"


@Route.get("/flash/")
@admin_only()
def flashed():
    flash("test", "info")
    flash("test", 'warning')
    flash("test", 'error')
    return render_template("root.html")


@Route.get("/moderator")
@role_required("moderator")
def moderator():
    return "true"
