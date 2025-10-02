from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.connection import get_db
from service.auth import AuthService

router = APIRouter()

@router.post("/")
def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    auth = AuthService.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if auth:
        access_token = AuthService.create_access_token(data={"sub": auth.username, "role": auth.role, "user_id": auth.id})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")