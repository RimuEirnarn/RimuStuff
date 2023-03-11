"""User Skeleton"""
# pylint: disable=unnecessary-ellipsis,too-few-public-methods
from typing import Protocol


class UserSkeleton(Protocol):
    """User Skeleton. Used for *Interface, as example for UserInterface"""
    @classmethod
    def get(cls, user_id: str):
        """Return user instance"""
        ...
