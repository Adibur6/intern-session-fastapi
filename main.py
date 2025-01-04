# create a fastapi main.py file a with cors middleware and get rooutes from routes folder
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.messages import router as message_router
from routes.users import router as user_router

app = FastAPI()

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




