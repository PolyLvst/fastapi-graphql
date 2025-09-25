import strawberry

@strawberry.input
class UserInput:
    username: str
    password: str
    instagram: str
    email: str
    bio: str