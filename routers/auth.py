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

router = APIRouter(
    prefix='/auth',
    tags=['auth']
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

SECRET_KEY = 'Zx7$wR!3M2q#L8uH%@fD9vE&cS0Jp^'
ALGORITHM = 'HS256'


class UserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    email: str = Field(min_length=1, max_length=30)
    password: str
    role: str = Field(min_length=1, max_length=30)


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db: db_dependency):
    """
    Check if user exists in the DB. If not, it returns False.  If it is in the DB, it checks
    the password.
    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, user_role: str, expire_time: timedelta):
    """
    Create the access JWT token and encode username, id, role and expiration in it.
    """
    expires = datetime.now(UTC) + expire_time
    encode = {'sub': username, 'id': user_id, 'role': user_role, 'exp': expires}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Get current user to check whether the token is still valid, or if it has been altered.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'user_id': user_id, 'user_role': user_role}
    
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')


@router.post('/user')
def create_user(db: db_dependency, new_user_request: UserRequest):
    """
    Creates a new user and adds it to the Users table.
    """
    new_user = Users(
    username = new_user_request.username,
    email = new_user_request.email,
    hashed_password = bcrypt_context.hash(new_user_request.password),
    role = new_user_request.role
    )

    db.add(new_user)
    db.commit()

@router.post('/token', response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                           db: db_dependency):
    """
    Authenticate a user and return a JWT access token.
    This endpoint validates the provided username and password against the database.
    If the credentials are correct, it generates a JWT token valid for 20 minutes.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}