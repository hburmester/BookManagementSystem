from uuid import uuid4
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, ValidationError, UUID4

class Book(BaseModel):
    title: str = Field(...)
    author: str = Field(...)
    published_date: date = Field(...)
    genre: str = Field(...)
    price: float = Field(...)

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[date]
    genre: Optional[str]
    price: Optional[float]
    
class UserCheck(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    token: str | None = None

class TokenData(BaseModel):
    token: str | None = None