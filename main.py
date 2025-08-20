from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from models import Books
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    status: bool
    progress: int

@app.get('/books')
def read_all(db: db_dependency):
    return db.query(Books).all()

@app.post('/books/')
def add_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.model_dump())
    
    db.add(book_model)
    db.commit()
