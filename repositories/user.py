from sqlalchemy.orm import Session
from model.database_model import User

class UserRepo:

    def list_users(db: Session) -> list[User]:
        return db.query(User).all()
    
    def get_user_by_id(db: Session, id: int) -> None | User:
        return db.query(User).filter(User.id == id).first()
    
    def get_user_by_username(db: Session, username: str) -> None | User:
        return db.query(User).filter(User.username == username).first()