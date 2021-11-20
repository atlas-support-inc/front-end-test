import sqlalchemy

from typing import List, Optional

from fastapi import Form, HTTPException, Depends, APIRouter
from fastapi.security import APIKeyCookie
from jose import jwt
from pydantic import BaseModel
from starlette.responses import Response, HTMLResponse
from starlette import status

from database import metadata, database


users_router = APIRouter()

cookie_sec = APIKeyCookie(name="session")

secret_key = "someactualsecret"

user_db = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String)
)


class User(BaseModel):
    id: Optional[int]
    username: str
    password: str


async def get_current_user(session: str = Depends(cookie_sec)):
    payload = jwt.decode(session, secret_key)
    username = payload["sub"]
    query = user_db.select().filter(user_db.c.username == username)
    data = await database.fetch_all(query)
    return data[0][0]


@users_router.get("/test_login_ui")
def login_page():
    return HTMLResponse(
        """
        <form action="/auth/login" method="post">
        Username: <input type="text" name="username" required>
        <br>
        Password: <input type="password" name="password" required>
        <input type="submit" value="Login">
        </form>
        """
    )


@users_router.post("/auth/create_users")
async def create_users():
    users = [
        ['jon', 'test'],
        ['sam', 'test'],
        ['jane', 'test'],
        ['joe', 'test'],
    ]
    for username, password in users:
        query = user_db.insert().values(username=username, password=password)
        await database.execute(query)
    return {}


@users_router.post("/auth/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    query = user_db.select()
    users = await database.fetch_all(query)
    user_dict = {}
    for (id, username, password) in users:
        user_dict[username] = password

    if not user_dict.get(username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )
    db_password = user_dict[username]
    if not password == db_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user or password"
        )
    token = jwt.encode({"sub": username}, secret_key)
    response.set_cookie("session", token)
    return {"ok": True}


@users_router.get("/auth/me")
async def me(user_id: int = Depends(get_current_user)):
    query = user_db.select().filter(user_db.c.id == user_id)
    data = await database.fetch_all(query)
    return data[0]


@users_router.get("/auth/users", response_model=List[User])
async def users(user_id: int = Depends(get_current_user)):
    query = user_db.select().filter(user_db.c.id != user_id)
    return await database.fetch_all(query)
