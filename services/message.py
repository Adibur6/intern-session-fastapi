from sqlalchemy.orm import Session
from models.message import Message
from models.user import User
from schemas.message import MessageCreate, MessageUpdate
from fastapi import HTTPException

class MessageService:
    @staticmethod
    def get_messages(current_user: User, db: Session):
        return db.query(Message).filter((Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)).all()

    @staticmethod
    def get_message(message_id: int, current_user: User, db: Session):
        message = db.query(Message).filter(Message.id == message_id).first()
        if message is None or (message.sender_id != current_user.id and message.receiver_id != current_user.id):
            raise HTTPException(status_code=404, detail="Message not found or access denied")
        return message

    @staticmethod
    def create_message(message: MessageCreate, current_user: User, db: Session):
        db_message = Message(content=message.content, sender_id=current_user.id, receiver_id=message.receiver_id)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def update_message(message_id: int, message: MessageUpdate, current_user: User, db: Session):
        db_message = db.query(Message).filter(Message.id == message_id).first()
        if db_message is None or db_message.sender_id != current_user.id:
            raise HTTPException(status_code=404, detail="Message not found or access denied")
        db_message.content = message.content
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def delete_message(message_id: int, current_user: User, db: Session):
        db_message = db.query(Message).filter(Message.id == message_id).first()
        if db_message is None or db_message.sender_id != current_user.id:
            raise HTTPException(status_code=404, detail="Message not found or access denied")
        db.delete(db_message)
        db.commit()
        return db_message