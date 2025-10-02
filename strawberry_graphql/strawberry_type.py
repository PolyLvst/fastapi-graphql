import strawberry
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    username: str
    role: str
    instagram: str | None
    email: str | None
    bio: str | None
    created_at: datetime