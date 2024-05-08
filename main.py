from fastapi import FastAPI
from routes.todo_routes import router as todo_router
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(todo_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
async def read_root():
    return "Hello world"