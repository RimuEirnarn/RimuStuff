"""Errors"""


class ApplicationError(Exception):
    """Application Error"""


class ApplicationErrorGroup(ExceptionGroup):
    """Application Error Group"""


class ResourceNotFound(ApplicationError):
    """Resource not found"""
