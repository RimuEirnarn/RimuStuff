"""Api Route"""
# pylint: disable=missing-function-docstring,missing-class-docstring
from flask import Blueprint, jsonify
from future_router import Router

Route = Router(Blueprint("api", __name__, url_prefix="/api"))


@Route.get('/')
def root():
    return jsonify({
        'status': 'success',
        'message': "Hello, World"
    })
