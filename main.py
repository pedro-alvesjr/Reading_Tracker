from typing import Annotated
from fastapi import Depends, FastAPI
from .models import Book
from .database import SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]