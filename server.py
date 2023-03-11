"""Server program"""

try:
    from app import create_app, register_login
    from app.bootstrap import bootstrap, register
    from app.route import Route
    from app.api_route import Route as ApiRoute
except ImportError:
    from .app import create_app, register_login
    from .app.bootstrap import bootstrap, register
    from .app.route import Route
    from .app.api_route import Route as ApiRoute

app = create_app()

register(register_login)
register(Route.init_app)
register(ApiRoute.init_app)
bootstrap(app)

if __name__ == '__main__':
    app.run("0.0.0.0", 8000, True)
