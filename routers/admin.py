from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Users, Books
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from routers.auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/books/all', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    """
    Retrieve all books.
    """
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User not authenticated.')
    
    return db.query(Books).all()