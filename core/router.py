"""Basic extended version of routing."""

from typing import Callable, Optional
from flask import Blueprint, Flask

try:
    from core.errors import NotResourcceClass, BlueprintError
    from core.typings import DefaultRoute, Function, ResourceRoute, ResourceT, Routes

    from core.utils import FrozenDict, multiple_hasattr
except ImportError:
    from .errors import NotResourcceClass, BlueprintError
    from .typings import DefaultRoute, Function, ResourceRoute, ResourceT, Routes

    from .utils import FrozenDict, multiple_hasattr

RESOURCE_METHODS = ('index', 'update', 'store', 'edit', 'create', 'update')
RESOURCE_MAP = FrozenDict(
    zip(RESOURCE_METHODS, ("/", "/", "/", "/<id>/edit", "/create", "/<id>")))


class Router:
    """Router class"""

    def __init__(self, blueprint: Optional[Blueprint] = None) -> None:
        self._app: Optional[Flask] = None
        self._pending_routes: list[Routes] = []
        self._pending_resources: list[ResourceRoute] = []
        self._pending_defaultroute: list[DefaultRoute] = []
        self._push_blueprint: bool = isinstance(blueprint, Blueprint)
        self._blueprint: Optional[Blueprint] = blueprint  # type: ignore
        self._blueprint_was_pushed = False

    def init_app(self, app: Flask):
        """Initialise app"""
        self._app = app
        for item in self._pending_routes:
            self._push_to_app_fn(item)
        self._pending_routes = []
        for item in self._pending_resources:
            self._push_to_app_res(item)
        self._pending_resources = []
        for item in self._pending_defaultroute:
            self._push_to_app(item)
        self._pending_defaultroute = []
        if self._blueprint:
            self._app.register_blueprint(self._blueprint)
            self._blueprint_was_pushed = True

    def init_blueprint(self, blueprint: Blueprint):
        """Initialise a blueprint"""
        self._push_blueprint = True
        self._blueprint: Blueprint = blueprint

    def pushable(self):
        """Is the Router instance can be pushed?"""
        try:
            self.get_app()
            return True
        except RuntimeError:
            return False
        except Exception:  # pylint: disable=try-except-raise
            raise

    def get_app(self) -> Blueprint | Flask:
        """Get current App. it's either Flask or Blueprint instance."""
        if not self._blueprint and self._push_blueprint:
            raise ValueError(
                "Cannot return blueprint, push blueprint was set to false.")
        if self._blueprint and self._push_blueprint:
            return self._blueprint
        if self._app:
            return self._app
        raise RuntimeError("Cannot return blueprint or app.")

    def _push_to_app(self, item: DefaultRoute):
        if self.pushable() is False:
            raise ValueError(
                "This must not be happening. This line must never be reached!")
        endpoint = item.option.pop('endpoint', None)
        self._add_url_rule(item.rule, endpoint,
                           item.view_func, **item.option)

    def _add_url_rule(self,
                      rule: str,
                      endpoint: Optional[str] = None,
                      func: Optional[Function] = None,
                      **options):
        """Seek out `Flask.add_url_rule` for more information"""
        if self._blueprint_was_pushed:
            raise BlueprintError(
                "New route cannot be registered anymore. Blueprint was pushed.")
        return self.get_app().add_url_rule(rule, endpoint, func, **options)

    def _push_to_app_fn(self, item: Routes):
        if self.pushable() is False:
            raise ValueError(
                "This must not be happening. This line must never be reached!")
        endpoint = item.kwargs.pop("endpoint", None)
        method: list[str] = item.kwargs.get("methods", [item.method])
        if item.method not in method:
            method.append(item.method)
        item.kwargs['methods'] = method
        self._add_url_rule(item.rule, endpoint, item.func, **item.kwargs)

    def _push_to_app_res(self, item: ResourceRoute):
        if self.pushable() is False:
            raise ValueError(
                "This must not be happening. This line must never be reached!")
        res_class = item.resource_class
        for key, value in RESOURCE_MAP.items():
            endpoint = f"{res_class.__name__}.{key}"
            rule = f"{item.rule}{value}"
            self._add_url_rule(rule, endpoint, getattr(res_class, key))

    def _put_pending_or_push(self, item: Routes | ResourceRoute):
        if self.pushable() is False:
            if isinstance(item, Routes):
                return self._pending_routes.append(item)
            return self._pending_resources.append(item)
        if isinstance(item, Routes):
            return self._push_to_app_fn(item)
        return self._push_to_app_res(item)

    def get(self, rule: str, *args, **kwargs):
        """Provide GET route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("GET", rule, func, args, kwargs))
            return func
        return wrapper

    def post(self, rule: str, *args, **kwargs):
        """Provide POST route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("POST", rule, func, args, kwargs))
            return func
        return wrapper

    def head(self, rule: str, *args, **kwargs):
        """Provide HEAD route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("HEAD", rule, func, args, kwargs))
            return func
        return wrapper

    def put(self, rule: str, *args, **kwargs):
        """Provide PUT route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("PUT", rule, func, args, kwargs))
            return func
        return wrapper

    def patch(self, rule: str, *args, **kwargs):
        """Provide PATCH route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("PATCH", rule, func, args, kwargs))
            return func
        return wrapper

    def delete(self, rule, *args, **kwargs):
        """Provide PUT route"""
        def wrapper(func: Callable):
            self._pending_routes.append(
                Routes("DELETE", rule, func, args, kwargs))
            return func
        return wrapper

    def resource(self, rule: str, *args, **kwargs):
        """Provide resource route.
        To make resource route, a class with these methods must exists"""
        def wrapper(class_: ResourceT):
            if not multiple_hasattr(class_, RESOURCE_METHODS):
                raise NotResourcceClass(
                    f"class {class_.__name__} Does not have all required functions.")
            self._pending_resources.append(
                ResourceRoute(class_, rule, args, kwargs))
            return class_
        return wrapper

    def route(self, rule: str, **options):
        """Please refer to `Flask.route` for more information."""
        def wrapper(func: Function):
            if self.pushable():
                endpoint = options.pop('endpoint', None)
                self._add_url_rule(rule, endpoint, func, **options)
                return func
            self._pending_defaultroute.append(
                DefaultRoute(rule, func, options))
            return func
        return wrapper
