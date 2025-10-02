import strawberry
from enum import Enum

@strawberry.enum
class RoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"

@strawberry.input
class UserCreate:
    username: str
    password: str
    role: RoleEnum = RoleEnum.USER
    instagram: str | None = None
    email: str | None = None
    bio: str | None = None

@strawberry.input
class UserUpdateBase:
    username: str | None = None
    password: str | None = None
    instagram: str | None = None
    email: str | None = None
    bio: str | None = None

@strawberry.input
class UserUpdate(UserUpdateBase):
    role: RoleEnum | None = None