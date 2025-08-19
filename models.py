from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Books(BaseModel):
    __tablename__ = 'books'
    
    id = Column(Integer)
    title = Column(String, default = 'Unknown')
    author = Column(String)
    status = Column(Boolean, default = True)
    progress = Column(Integer)

