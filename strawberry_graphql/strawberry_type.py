import strawberry
from datetime import datetime

@strawberry.type
class UserType:
    id: int
    username: str
    instagram: str
    email: str
    bio: str
    created_at: datetime