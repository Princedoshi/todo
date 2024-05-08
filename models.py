from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Todo(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    due_date: datetime
    completed: bool

class User(BaseModel):
    username: str
    email: str
    password_hash: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str