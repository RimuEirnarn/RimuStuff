"""Api Route"""
# pylint: disable=missing-function-docstring,missing-class-docstring
from flask import Blueprint, jsonify

try:
    from . import Router
except ImportError:
    from app import Router

Route = Router(Blueprint("api", __name__, url_prefix="/api"))


@Route.get('/')
def root():
    return jsonify({
        'status': 'success',
        'message': "Hello, World"
    })
