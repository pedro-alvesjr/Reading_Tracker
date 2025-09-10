from datetime import UTC, datetime, timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Books, Users
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from routers.auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class PasswordVerification(BaseModel):
    current_password: str
    new_password: str = Field(min_length=5)

@router.get('/user', status_code=status.HTTP_200_OK)
def get_user(user: user_dependency, 
             db: db_dependency):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='User not authenticated.'
            )
    
    return db.query(Users).filter(Users.id == user.get('id')).first()