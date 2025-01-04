from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    fullname: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    fullname: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str