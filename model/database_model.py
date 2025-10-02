from datetime import datetime
import pytz
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(255), default="user") # roles: user, admin
    instagram = Column(String(255))
    email = Column(String(255))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))