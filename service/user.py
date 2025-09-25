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

    def delete_user(id: int) -> str:
        with get_db_context() as db:
            user = db.query(User).filter(User.id == id).first()
            if user:
                db.delete(user)
                db.commit()
                return "User deleted"
            return "User not found"

    def update_user(id: int, user: UserInput) -> User | None:
        with get_db_context() as db:
            existing_user = db.query(User).filter(User.id == id).first()
            if not existing_user:
                return None

            for key, value in user.__dict__.items():
                if value is not None:
                    setattr(existing_user, key, value)

            if user.password:
                existing_user.password_hash = f"{user.password}_HASH"

            db.commit()
            db.refresh(existing_user)
            return existing_user
    
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