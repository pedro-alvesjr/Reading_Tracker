from fastapi import FastAPI
from database import Base, SessionLocal, engine
from routers import books, auth, users
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(books.router)
app.include_router(auth.router)
app.include_router(users.router)