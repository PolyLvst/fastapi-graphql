from enum import Enum
from config.connection import get_db_context
from model.database_model import User
from repositories.user import UserRepo
from service.auth import AuthService
from strawberry_graphql.strawberry_input import UserCreate, UserUpdateBase

class UserService:

    def list_users() -> list[User]:
        with get_db_context() as db:
            return UserRepo.list_users(db=db)

    def get_user_by_id(id: int) -> User:
        with get_db_context() as db:
            return UserRepo.get_user_by_id(db=db, id=id)

    def delete_user(id: int) -> str:
        with get_db_context() as db:
            user = UserRepo.get_user_by_id(db=db, id=id)
            if user:
                db.delete(user)
                db.commit()
                return "User deleted"
            return "User not found"

    def update_user(id: int, user: UserUpdateBase) -> User | None:
        with get_db_context() as db:
            existing_user = UserRepo.get_user_by_id(db=db, id=id)
            if not existing_user:
                return None

            for key, value in user.__dict__.items():
                if value is not None:
                    setattr(existing_user, key, value)

            if user.password:
                existing_user.password_hash = AuthService.get_password_hash(user.password)

            db.commit()
            db.refresh(existing_user)
            return existing_user
    
    def create_user(user: UserCreate) -> User:
        with get_db_context() as db:
            user_kwargs = user.__dict__.copy()
            user_kwargs['password_hash'] = AuthService.get_password_hash(user_kwargs['password'])
            del user_kwargs['password']

            # Convert Enum to str before passing to SQLAlchemy
            if isinstance(user_kwargs["role"], Enum):
                user_kwargs["role"] = user_kwargs["role"].value

            user = User(**user_kwargs)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user