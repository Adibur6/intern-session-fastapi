from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db.connection import get_db
from models.message import Message
from models.user import User
from schemas.message import MessageCreate, MessageUpdate, MessageResponse
from typing import List
from typing_extensions import Annotated
from auth.jwt_handler import decode_access_token
from services.message import MessageService
import logging

router = APIRouter()

def get_current_user(token: str, db: Session):
    try:
        logging.info(f"token: {token}")
        scheme, token = token.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        payload = decode_access_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/messages", response_model=List[MessageResponse])
async def get_messages(token: Annotated[str,Header()], db: Session = Depends(get_db)):
    logging.info(f"Current user: {token}")
    current_user = get_current_user(token, db)
    messages = MessageService.get_messages(current_user, db)
    return messages

@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, token: Annotated[str,Header()], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    message = MessageService.get_message(message_id, current_user, db)
    return message

@router.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate, token: Annotated[str,Header()], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    db_message = MessageService.create_message(message, current_user, db)
    return db_message

@router.patch("/messages/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, message: MessageUpdate, token: Annotated[str,Header()], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    db_message = MessageService.update_message(message_id, message, current_user, db)
    return db_message

@router.delete("/messages/{message_id}", response_model=MessageResponse)
async def delete_message(message_id: int, token: Annotated[str,Header()], db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    db_message = MessageService.delete_message(message_id, current_user, db)
    return db_message