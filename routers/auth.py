from datetime import UTC, datetime, timedelta
from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Books, Users
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
    username: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=30)
    password: str
    role: str = Field(min_length=1, max_length=30)


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True


def create_access_token(username: str, user_id: int, user_role: str, expire_time: timedelta):
    expires = datetime.now(UTC) + expire_time
    encode = {'sub': username, 'id': user_id, 'role': user_role, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post('/user')
def create_user(db: db_dependency, new_user_request: UserRequest):
    
    new_user = Users(
    username = new_user_request.username,
    email = new_user_request.email,
    hashed_password = bcrypt_context.hash(new_user_request.password),
    role = new_user_request.role
    )

    db.add(new_user)
    db.commit()