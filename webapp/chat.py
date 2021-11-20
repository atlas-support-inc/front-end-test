import sqlalchemy
from sqlalchemy import or_
from typing import List, Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import metadata, database
from users import get_current_user

chat_router = APIRouter()

chat_db = sqlalchemy.Table(
    "chat",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("from_user_id", sqlalchemy.Integer),
    sqlalchemy.Column("to_user_id", sqlalchemy.Integer),
    sqlalchemy.Column("message", sqlalchemy.String),
)


class Chat(BaseModel):
    id: Optional[int]
    from_user_id: Optional[int]
    to_user_id: int
    message: str


@chat_router.get("/chat/list", response_model=List[Chat])
async def users(user_id: str = Depends(get_current_user)):
    query = chat_db.select().filter(
        or_(chat_db.c.from_user_id == user_id,
            chat_db.c.to_user_id == user_id))
    return await database.fetch_all(query)


@chat_router.post("/chat/create")
async def chat(to_user_id: int, message: str, user_id: str = Depends(get_current_user)):
    query = chat_db.insert().values(
        from_user_id=user_id,
        to_user_id=to_user_id,
        message=message
    )
    await database.execute(query)
    from ws import manager
    await manager.send_new_chat(to_user_id)
    return {}
