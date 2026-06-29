import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from database import engine, Base, get_session
from typing import Annotated
import models 
from models import config
from pydantic import BaseModel, Field 
from security import get_password_hash, verify_password
from authx import AuthX, AuthXConfig
import json

app = FastAPI()

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = config["JWT_KEY"]
auth_config.JWT_ACCESS_COOKIE_NAME = "english_access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

auth_security = AuthX(config=auth_config)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class UserSchema(BaseModel):
    name: str = Field(min_length=5, max_length=15)
    raw_password: str = Field(min_length=5, max_length=20)
    
class UserAddSchema(BaseModel):
    name: str
    hashed_password: str
    @classmethod
    def hash_password(cls, name: str, raw_password: str):
        return cls(name= name, hashed_password = get_password_hash(raw_password))
    
# @app.post("/setup_database")
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     return {"ok": True}

@app.post("/login")
async def login(creds: UserSchema, response: Response, session: SessionDep):
    query = select(models.User.id, models.User.name, models.User.hashed_password).where(
        models.User.name == creds.name
    )
    result = await session.execute(query)
    result = result.mappings().first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Такого пользователя нет!")
    if creds.name == result["name"] and verify_password(creds.raw_password, result["hashed_password"]):
        token = auth_security.create_access_token(uid=str(result["id"]))
        response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail= "incorrect name or password")

# @app.get("/protected", dependencies=[Depends(auth_security.access_token_required)])
# async def protected():
#     return {"secret":"goddamn yeah"}


@app.post("/add_user")
async def add_user(data: UserSchema, session: SessionDep):
    user_in_db = UserAddSchema.hash_password(name= data.name,
                                             raw_password=data.raw_password)
    check_query = select(models.User.id).where(models.User.name == data.name)
    check_result = await session.execute(check_query)
    user_exists = check_result.scalar_one_or_none()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже зарегистрирован"
        )
    
    new_user = models.User(**user_in_db.model_dump())
    session.add(new_user)
    await session.commit()
    return {"Champion" : True}

@app.get("/get_user/{name}")
async def get_user(name: str, session: SessionDep):
    query = select(models.User.name, models.User.id,
                   models.User.hashed_password).where(models.User.name == name)
    result = await session.execute(query)
    return result.mappings().all()

@app.get("/get_users")
async def get_users(session: SessionDep):
    query = select(models.User)
    result = await session.execute(query)
    result = result.mappings().all()
    return result

# @app.post("/drop_users")
# async def drop_users():
#     async with engine.begin () as conn:
#         await conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE;"))
        
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
