from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from models import Books
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session

router = APIRouter()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class BookRequest(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    author: str = Field(min_length=1, max_length=30)
    status: bool
    progress: int = Field(gt=-1, lt=101)

@router.get('/books')
def read_all(db: db_dependency):
    return db.query(Books).all()


@router.get('/books/{book_id}')
def read_by_id(db: db_dependency, book_id: int = Path(gt=0)):
    return db.query(Books).filter(Books.id == book_id).first()


@router.post('/books')
def add_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.model_dump())
    
    db.add(book_model)
    db.commit()

@router.put('/books/{book_id}')
def update_book(db: db_dependency, book_request: BookRequest, book_id: int = Path(gt=0)):
    updated_book = db.query(Books).filter(Books.id == book_id).first()

    if updated_book is None:
        raise HTTPException(status_code=404, detail='Book ID not found.')

    updated_book.title = book_request.title
    updated_book.author = book_request.author
    updated_book.status = book_request.status
    updated_book.progress = book_request.progress

    db.commit()

@router.delete('/books/{book_id}')
def delete_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_to_delete = db.query(Books).filter(Books.id == book_id).first()
    
    if book_to_delete is None:
        raise HTTPException(status_code=404, detail='Book ID not found.')

    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()