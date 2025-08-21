from typing import Annotated
from fastapi import Depends, FastAPI, Path
from pydantic import BaseModel, Field
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
    title: str = Field(min_length=1, max_length=30)
    author: str = Field(min_length=1, max_length=30)
    status: bool
    progress: int = Field(gt=-1, lt=101)

@app.get('/books')
def read_all(db: db_dependency):
    return db.query(Books).all()


@app.get('/books/{book_id}')
def read_by_id(db: db_dependency, book_id: int = Path(gt=0)):
    return db.query(Books).filter(Books.id == book_id).first()


@app.post('/books/')
def add_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.model_dump())
    
    db.add(book_model)
    db.commit()

