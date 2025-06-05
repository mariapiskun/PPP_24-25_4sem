from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    year: int = Field(..., ge=0, le=datetime.now().year)
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class AuthorWithBooks(Author):
    books: List[Book] = [] 