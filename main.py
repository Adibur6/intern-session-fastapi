from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from routes.messages import router as message_router
from routes.users import router as user_router
from db.connection import Base, engine

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(message_router)

origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

