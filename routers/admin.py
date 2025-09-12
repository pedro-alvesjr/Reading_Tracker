from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Users
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
