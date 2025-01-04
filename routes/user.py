# create a users router to create, get and login users

from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"users": "This is a list of users"}

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@router.post("/users")
async def create_user():
    return {"user": "User has been created"}

@router.post("/users/login")
async def login_user():
    return {"user": "User has been logged in"}

