"""User Model"""
from flask_login import UserMixin
from sqlite_database import op

try:
    from ..errors import ResourceNotFound
    from ..database_loader import table
    from . import BaseModel
except ImportError:
    from app.errors import ResourceNotFound
    from app.database_loader import table
    from app.model import BaseModel


class UserModel(BaseModel, table=table('users')):  # type: ignore
    """User Model"""
    username: str
    password: str
    picture: str
    groups: str

    """User Model"""
    @classmethod
    def load(cls, user_id: str):
        """Load from user_id"""
        user = cls._table.select_one(  # type: ignore
            {"username": op == user_id})
        if user:
            return UserModel(user)
        raise ResourceNotFound(f"Resource for {user_id} is not found")

    @staticmethod
    def find(user_id: str):
        return UserModel.load(user_id)

    @staticmethod
    def all():
        return UserModel._table.select()


class UserInterface(UserMixin):  # type: ignore
    """User Model Interface"""

    def __init__(self, __user: UserModel | str) -> None:
        super().__init__()
        if isinstance(__user, UserModel):
            self._data = __user
            return
        if not __user:
            raise ValueError("User must not be null")
        self._data = UserModel.load(__user)

    @property
    def is_authenticated(self):
        """Is Authenticated"""
        return True

    @classmethod
    def get(cls, user_id: str):
        """Get UserModel by Id"""
        return cls(user_id)

    def get_id(self) -> str:
        """Get user id"""
        return self._data.username
