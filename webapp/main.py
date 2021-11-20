
from fastapi import FastAPI

from chat import chat_router
from database import metadata, engine
from users import users_router
from ws import ws_router

app = FastAPI()
app.include_router(users_router)
app.include_router(chat_router)
app.include_router(ws_router)

metadata.create_all(engine)
