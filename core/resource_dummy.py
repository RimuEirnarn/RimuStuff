"""Resource Dummy"""
from typing import Protocol


class ResourceDummy(Protocol):
    """Resource Dummy"""

    def index(self):
        """Index all the resource available."""

    def create(self):
        """Show the user/form response"""

    def store(self):
        """Store user request"""

    def edit(self):
        """Show user edit form response."""

    def update(self):
        """Update user request"""

    def delete(self):
        """Delete user request"""
