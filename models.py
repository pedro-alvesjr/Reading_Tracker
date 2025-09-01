from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Books(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default = 'Unknown')
    author = Column(String)
    status = Column(Boolean, default = True)
    progress = Column(Integer)

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)