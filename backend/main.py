import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, insert
from database import engine, Base, get_session
from typing import Annotated
import models 
from models import config
from pydantic import BaseModel, Field 
from security import get_password_hash, verify_password
from authx import AuthX, AuthXConfig
import json
import googletrans

app = FastAPI()

translator = googletrans.Translator()

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = config["JWT_KEY"]
auth_config.JWT_ACCESS_COOKIE_NAME = "english_access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

auth_security = AuthX(config=auth_config)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class UserFrontendSchema(BaseModel):
    name: str = Field(min_length=5, max_length=15)
    raw_password: str = Field(min_length=5, max_length=20)
    
class UserDBSchema(BaseModel):
    name: str
    hashed_password: str
    @classmethod
    def hash_password(cls, name: str, raw_password: str):
        return cls(name= name, hashed_password = get_password_hash(raw_password))
   
class WordFrontendSchema(BaseModel):
    origin: str = Field(min_length=2, max_length=20)
    is_origin_english: bool = True

class WordDBSchema(BaseModel):
    english_word: str
    russian_word: str 
    @classmethod
    async def translate_word(cls, origin: str, is_orig_eng: bool):
        if is_orig_eng:
            _english_word = origin
            _russian_word = await translator.translate(origin, src="en", dest="ru")
            _russian_word = _russian_word.text
        else:
            _russian_word = origin
            _english_word = await translator.translate(origin, src="ru", dest="en") 
            _english_word = _english_word.text
        return cls(origin= origin,english_word=_english_word, russian_word= _russian_word)
     
# @app.post("/setup_database")
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     return {"ok": True}

@app.post("/login")
async def login(creds: UserFrontendSchema, response: Response, session: SessionDep):
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

@app.post("/add_word")
async def add_word(data: WordFrontendSchema, session: SessionDep):
    data.origin = data.origin.lower()
    data_to_db = await WordDBSchema.translate_word(data.origin, data.is_origin_english)
    query = insert(models.Word_Info).values(origin= data_to_db.english_word,
                                            translation= data_to_db.russian_word)
    result = await session.execute(query)
    await session.commit()
    return {"result": result}

@app.post("/add_user")
async def add_user(data: UserFrontendSchema, session: SessionDep):
    user_in_db = UserDBSchema.hash_password(name= data.name,
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

async def execute_query(query, session):
     result = await session.execute(query)
     return result.mappings().all()

@app.get("/get_user/{name}")
async def get_user(name: str, session: SessionDep):
    query = select(models.User.name, models.User.id,
                   models.User.hashed_password).where(models.User.name == name)
    result = await execute_query(query, session)
    return result

@app.get("/get_users")
async def get_users(session: SessionDep):
    query = select(models.User)
    result = await execute_query(query, session)    
    return result

@app.get("/get_words")
async def get_words(session: SessionDep):
    query = select(models.Word_Info)
    result = await execute_query(query, session)
    return result

@app.post("/drop")
async def drop():
    async with engine.begin () as conn:
        await conn.execute(text("TRUNCATE TABLE words_info RESTART IDENTITY CASCADE;"))
        
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)