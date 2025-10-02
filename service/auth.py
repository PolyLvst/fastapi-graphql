import secrets
from uuid import uuid4
from fastapi import HTTPException, Request, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from config.connection import get_db_context
from model.database_model import User
from repositories.user import UserRepo

SECRET_KEY = "YOUR_SUPER_SECRET_KEY_HERE_PLEASE_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")

    # Get Context for GraphQL
    async def get_context(request: Request) -> dict:
        auth_header = request.headers.get("Authorization")
        user = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = AuthService.get_current_user(token)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing or malformed",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        # PolyLvst; Current user can be None if no token provided or a non protected route
        return {"current_user": user}

    def get_current_user(token: str):
        payload = AuthService.verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    
    def allowed_roles_only(allowed_roles: list[str], current_user: dict):
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if not current_user.get("role") in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Must be one of these roles {allowed_roles} only")
        return current_user
    
    def verify_password(plain_password, hashed_password):
        return AuthService.pwd_context.verify(plain_password,hashed_password)

    def get_password_hash(password):
        return AuthService.pwd_context.hash(password)

    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

    def authenticate_user(db:Session, username, password):
        current_username = username
        try:
            account = UserRepo.get_user_by_username(db=db, username=username)
        except:
            account = None
        if account:
            correct_username = account.username
            # To prevent timing attack
            is_correct_username = secrets.compare_digest(current_username, correct_username)
            is_correct_password = AuthService.verify_password(password, account.password_hash)
            if not (is_correct_username and is_correct_password):
                return False
            return account
        else:
            # To prevent timing attack
            if not secrets.compare_digest("unknown","user"):
                return False
    
    def create_admin_if_not_exists():
        with get_db_context() as db:
            admin_username = "graphql-admin"
            password = "graphql-admin"
            admin_role = "admin"
            # Check if atleast one admin present
            user = db.query(User).filter(User.role == admin_role).first()
            if user is not None:
                print(f"STARTUP:  #- OKAY detected atleast one admin user")
                return
            # Check for dupe username previous admin
            dupe_admin = db.query(User).filter(User.username == admin_username).first()
            if dupe_admin:
                print(f"STARTUP:  #- DUPE detected previous admin user {admin_username}")
                dupe_admin.username = f"{admin_username}-{uuid4()}"
                db.commit()
                db.refresh(dupe_admin)
                print(f"STARTUP:  #- RENAMED previous admin user {admin_username}")
            
            # Begin admin creation
            user = User(username=admin_username,
                        password_hash=AuthService.get_password_hash(password),
                        role=admin_role)
            try:
                db.add(user)
                db.commit()
                print(f"STARTUP:  #- Generated admin user")
                print(f"STARTUP:  #- username : {admin_username}")
                print(f"STARTUP:  #- password : {password}")
            except Exception as e:
                db.rollback()
                print(f"STARTUP:  #- Error : {e}")
                raise e