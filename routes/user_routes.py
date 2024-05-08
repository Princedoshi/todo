from fastapi import APIRouter, Depends
from database import users_collection
from models import User, UserCreate
from auth import pwd_context

router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    hashed_password = pwd_context.hash(user_data.password)
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "password_hash": hashed_password
    }
    users_collection.insert_one(new_user)
    return new_user

@router.get("/users", response_model=list[User])
async def get_users():
    users = []
    for user in users_collection.find():
        users.append(User(**user))
    return users