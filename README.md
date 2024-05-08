# Project: Todo App with FastAPI and PyMongo

This is a FastAPI application that provides a RESTful API for managing a todo list. It uses PyMongo as the database driver to interact with a MongoDB database. The application also includes JWT (JSON Web Token) authentication for secure access to the API endpoints.

## Dependencies

The project requires the following dependencies:

- `fastapi`: A modern, fast (high-performance), web framework for building APIs with Python.
- `pydantic`: A data validation library used by FastAPI.
- `python-multipart`: A library for handling form data in FastAPI.
- `pymongo`: The official Python driver for MongoDB.
- `bson`: A library for handling BSON (Binary JSON) data, which is used by PyMongo.
- `passlib`: A library for password hashing and verification.
- `python-jose`: A library for JSON Web Token (JWT) encoding and decoding.
- `bcrypt`: A library providing bcrypt hashing for passwords, used by Passlib.

You can install these dependencies by running `pip install -r requirements.txt` in your project directory.

## Project Structure

- `app.py`: The main FastAPI application file containing routes, models, and authentication functions.
- `requirements.txt`: A file listing the project dependencies and their versions.

## Database

The application uses a MongoDB database named `todo_db` with a collection called `todos`. The database connection is established using the `MongoClient` from PyMongo.

## Models

The application defines two Pydantic models:

1. `Todo`: Represents a todo item with fields such as `id`, `title`, `description`, `due_date`, and `completed`.
2. `User`: Represents a user with fields such as `username`, `email`, and `password_hash`.

## Authentication

The application implements JWT authentication for securing the API endpoints. The following functions are provided for authentication:

- `verify_password(plain_password, hashed_password)`: Verifies a plain-text password against a hashed password using Passlib.
- `get_user(username)`: Retrieves a user from the database based on the username.
- `authenticate_user(username, password)`: Authenticates a user by verifying the provided username and password.
- `create_access_token(data, expires_delta)`: Creates a JSON Web Token (JWT) with the provided data and expiration time.

## Routes

The application defines the following routes:

- `POST /token`: Authenticates a user and returns an access token.
- `POST /register`: Registers a new user.
- `GET /users`: Retrieves a list of all users.
- `GET /todos/{todo_id}`: Retrieves a todo item by its ID.
- `POST /todos/`: Creates a new todo item.
- `GET /todos`: Retrieves a list of all todo items.
- `PUT /todos/{todo_id}`: Updates an existing todo item.
- `DELETE /todos/{todo_id}`: Deletes a todo item.

## Usage

1. Start the MongoDB server on your local machine.
2. Run the FastAPI application with `uvicorn app:app --reload`.
3. Access the API endpoints using tools like Postman or cURL.

Note: Make sure to replace the `SECRET_KEY` in `app.py` with a secure secret key for your application.