from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str
    receiver_id: int

class MessageUpdate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    content: str
    sender_id: int
    receiver_id: int

    class Config:
        orm_mode = True