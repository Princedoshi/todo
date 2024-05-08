from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import todos_collection, db  # Import the db object
from models import Todo
from bson import ObjectId
from auth import authenticate_user, create_access_token
from fastapi import Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from models import UserCreate
from auth import pwd_context
from models import User
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# @router.get("/fetch_todo/{todo_id}", response_model=Todo)
# async def fetch_todo(todo_id: str):
#     try:
#         todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
#         if todo is None:
#             raise HTTPException(status_code=404, detail="Todo not found")
#         todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
#         return Todo(**todo)
#     except Exception as e:
#         return {"message": "Failed to fetch todo", "error": str(e)}

@router.get("/fetch_todo/{todo_id}", response_model=Todo)
async def fetch_todo(todo_id: str = Path(..., title="The ID of the todo to fetch")):
    try:
        # Perform a query to fetch the document from the collection
        todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Ensure all required fields are present in the response
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
        return Todo(**todo)
    except Exception as e:
        return {"message": "Failed to fetch todo", "error": str(e)}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    hashed_password = pwd_context.hash(user_data.password)

    # Create a new user object
    new_user = {
        "username": user_data.username,
        "email": user_data.email,
        "password_hash": hashed_password
    }

    # Insert the new user into the database
    db.users.insert_one(new_user)

    
    # Return the newly created user
    return new_user

@router.get("/users", response_model=list[User])
async def get_users():
    users = []
    for user in db.users.find():
        users.append(User(**user))
    return users

@router.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    # Verify token here if necessary
    todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**todo)

@router.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo, token: str = Depends(oauth2_scheme)):
    # Verify token here if necessary
    todo_dict = todo.dict()
    todo_dict.pop("id")
    todo_id = todos_collection.insert_one(todo_dict).inserted_id
    return Todo(**todo_dict, id=str(todo_id))

@router.get("/todos", response_model=list[Todo])
async def get_todos(token: str = Depends(oauth2_scheme)):
    todos = []
    for todo in todos_collection.find():
        todo["_id"] = str(todo["_id"])  # Convert ObjectId to string
        todos.append(Todo(**todo))
    return todos

@router.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_data: Todo, token: str = Depends(oauth2_scheme)):
    # Verify token here if necessary
    
    # Check if the todo exists
    existing_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update the todo
    updated_todo = {
        "id": todo_id,
        "title": todo_data.title,
        "description": todo_data.description,
        "due_date": todo_data.due_date,
        "completed": todo_data.completed
    }
    todos_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": updated_todo})
    
    return Todo(**updated_todo)

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, token: str = Depends(oauth2_scheme)):
    # Verify token here if necessary
    
    # Check if the todo exists
    existing_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Delete the todo
    todos_collection.delete_one({"_id": ObjectId(todo_id)})
    
    return {"message": "Todo deleted successfully"}
