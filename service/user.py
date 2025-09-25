from config.connection import get_db_context
from model.database_model import User
from strawberry_graphql.strawberry_input import UserInput

class UserService:

    def list_users() -> list[User]:
        with get_db_context() as db:
            return db.query(User).all()

    def get_user_by_id(id: int) -> User:
        with get_db_context() as db:
            return db.query(User).filter(User.id == id).first()
    
    def create_user(user: UserInput) -> User:
        with get_db_context() as db:
            user_kwargs = user.__dict__
            user_kwargs['password_hash'] = f"{user.password}_HASH"
            del user_kwargs['password']

            user = User(**user_kwargs)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user