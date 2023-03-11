"""utility"""
from tomllib import loads


def project_version():
    """Project version"""
    with open("project.toml", encoding='utf-8') as file:
        data = file.read()
    config = loads(data)
    return config.get("VERSION", config.get("BASE_VERSION"))
