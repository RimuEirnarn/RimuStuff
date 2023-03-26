"""Typings"""

from typing import Callable

from flask import Flask

BootstrapFunction = Callable[[Flask], None]
