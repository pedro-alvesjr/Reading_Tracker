from datetime import timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Books
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
password_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

SECRET_KEY = 'Zx7$wR!3M2q#L8uH%@fD9vE&cS0Jp^'
ALGORITHM = 'HS256'

class UserRequest(BaseModel):
    id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=30)
    hashed_password: str
    role: str = Field(min_length=1, max_length=30)