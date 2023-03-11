"""Typings"""

from typing import Any, Callable, NamedTuple, Type

from flask import Flask
from .resource_dummy import ResourceDummy

ResourceT = Type[ResourceDummy]
Function = Callable[..., Any]
Args = tuple[Any, ...]
Kwargs = dict[str, Any]
ResOrFunc = ResourceT | Function
BootstrapFunction = Callable[[Flask], None]
# ResourceRoute = tuple[ResourceT, Args, Kwargs]
# Routes = tuple[str, str, Function, Args, Kwargs]


class DefaultRoute(NamedTuple):
    """Default route"""
    rule: str
    view_func: Function
    option: Kwargs


class Routes(NamedTuple):
    """Routes"""
    method: str
    rule: str
    func: Function
    args: Args
    kwargs: Kwargs


class ResourceRoute(NamedTuple):
    """Resource Routes"""
    resource_class: ResourceT
    rule: str
    args: Args
    kwargs: Kwargs
