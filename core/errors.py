"""Errors"""


class NotResourcceClass(Exception):
    """A class is not a resource class."""


class BootstrapFailed(ExceptionGroup):
    """An error in bootstraping occured."""

class BlueprintError(Exception):
    """An error related to blueprint occured."""
