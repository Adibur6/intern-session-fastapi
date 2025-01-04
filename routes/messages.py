# create routes for messages 

from fastapi import APIRouter

router = APIRouter()

@router.get("/messages")
async def get_messages():
    return {"messages": "This is a list of messages"}

@router.get("/messages/{message_id}")
async def get_message(message_id: int):
    return {"message_id": message_id}

@router.post("/messages")
async def create_message():
    return {"message": "Message has been created"}

@router.put("/messages/{message_id}")
async def update_message(message_id: int):
    return {"message_id": message_id}

@router.delete("/messages/{message_id}")
async def delete_message(message_id: int):
    return {"message_id": message_id}