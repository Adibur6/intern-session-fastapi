from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db.connection import get_db
from models.message import Message
from models.user import User
from schemas.message import MessageCreate, MessageUpdate, MessageResponse
from typing import List
from auth.jwt_handler import decode_access_token

router = APIRouter()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    try:
        scheme, token = authorization.split()
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
async def get_messages(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = db.query(Message).filter((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)).all()
    return messages

@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None or (message.sender_id != current_user.id and message.receiver_id != current_user.id):
        raise HTTPException(status_code=404, detail="Message not found or access denied")
    return message

@router.post("/messages", response_model=MessageResponse)
async def create_message(message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_message = Message(content=message.content, sender_id=current_user.id, receiver_id=message.receiver_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.patch("/messages/{message_id}", response_model=MessageResponse)
async def update_message(message_id: int, message: MessageUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None or db_message.sender_id != current_user.id:
        raise HTTPException(status_code=404, detail="Message not found or access denied")
    db_message.content = message.content
    db.commit()
    db.refresh(db_message)
    return db_message

@router.delete("/messages/{message_id}", response_model=MessageResponse)
async def delete_message(message_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None or db_message.sender_id != current_user.id:
        raise HTTPException(status_code=404, detail="Message not found or access denied")
    db.delete(db_message)
    db.commit()
    return db_message