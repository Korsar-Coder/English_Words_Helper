import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, insert
from database import engine, Base, get_session
from typing import Annotated
import models 
from models import main_config
from pydantic import BaseModel, Field 
from security import get_password_hash, verify_password
from authx import AuthX, AuthXConfig, TokenPayload
import googletrans

import random

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],     
    )

translator = googletrans.Translator()

auth_config = AuthXConfig()
auth_config.JWT_SECRET_KEY = main_config["JWT_KEY"]
auth_config.JWT_ACCESS_COOKIE_NAME = "english_access_token"
auth_config.JWT_TOKEN_LOCATION = ["cookies"]

auth_config.JWT_COOKIE_SAMESITE = "none"  
auth_config.JWT_COOKIE_SECURE = True      

auth_config.JWT_COOKIE_CSRF_PROTECT = False 

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
    user_id: int
    origin: str = Field(min_length=2, max_length=20)
    translation: str = ""
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

@app.post("/api/login")
async def login(creds: UserFrontendSchema, response: Response, session: SessionDep):
    query = select(models.User.id, models.User.name, models.User.hashed_password).where(
        models.User.name == creds.name
    )
    result = await session.execute(query)
    result = result.mappings().first()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User doesn't exist")
    if creds.name == result["name"] and verify_password(creds.raw_password, result["hashed_password"]):
        token = auth_security.create_access_token(uid=str(result["id"]), data={
            "username" : creds.name, "role" : "user"
        })
        # response.set_cookie(auth_config.JWT_ACCESS_COOKIE_NAME, 
        #                     token, httponly=True,samesite="none",
        #                     secure= True 
        #                     )
        auth_security.set_access_cookies(token, response)
        return {"status": "success"}    
    raise HTTPException(status_code=401, detail= "incorrect name or password")

@app.post("/api/register")
async def register(creds: UserFrontendSchema, response: Response, session: SessionDep):
    query = select(models.User).where(
        models.User.name == creds.name
    )
    result = await session.execute(query)
    result = result.mappings().first()
    if result:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists!")
   
    user_in_db = UserDBSchema.hash_password(name= creds.name,
                                             raw_password= creds.raw_password) 
    new_user = models.User(**user_in_db.model_dump())
    session.add(new_user)
    
    token = auth_security.create_access_token(uid=str(new_user.id), data={
        "username" : creds.name, "role" : "user"
    })

    auth_security.set_access_cookies(token, response)
    await session.commit()
    return {"status": "success"}    

@app.post("/api/logout")
def logout(response: Response):
    auth_security.unset_access_cookies(response)
    return {"status" : "success", "message" : "Вы вышли из системы!"}

# @app.get("/protected", dependencies=[Depends(auth_security.access_token_required)])
# async def protected():
#     return {"secret":"goddamn yeah"}

@app.post("/api/add_word")
async def add_word(data: WordFrontendSchema, session: SessionDep):
    data.origin = data.origin.lower()
    if data.translation == "":
        data_to_db = await WordDBSchema.translate_word(data.origin, data.is_origin_english)
    else: 
        if data.is_origin_english:
            data_to_db = WordDBSchema(english_word=data.origin, russian_word=data.translation)
        else: 
            data_to_db = WordDBSchema(english_word=data.translation, russian_word=data.origin)
    query = insert(models.Users_word).values(origin= data_to_db.english_word,
                                            translation= data_to_db.russian_word,
                                            user_id= data.user_id)
    result = await session.execute(query)
    await session.commit()
    return {"result": result}

@app.post("/api/add_user")
async def add_user(data: UserFrontendSchema, session: SessionDep):
    user_in_db = UserDBSchema.hash_password(name= data.name,
                                             raw_password=data.raw_password)
    check_query = select(models.User.id).where(models.User.name == data.name)
    check_result = await session.execute(check_query)
    user_exists = check_result.scalar_one_or_none()
    
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    new_user = models.User(**user_in_db.model_dump())
    session.add(new_user)
    await session.commit()
    return {"Champion" : True}

async def execute_query(query, session):
     result = await session.execute(query)
     return result.mappings().all()

@app.get("/api/check-auth")
def check_auth(payload: TokenPayload = Depends(auth_security.access_token_required)):
    return {"authenticated": True,
            "user_id": payload.sub}

@app.get("/api/get_user/{name}")
async def get_user(name: str, session: SessionDep):
    query = select(models.User.name, models.User.id,
                   models.User.hashed_password).where(models.User.name == name)
    result = await execute_query(query, session)
    return result

@app.get("/api/get_users")
async def get_users(session: SessionDep):
    query = select(models.User)
    result = await execute_query(query, session)    
    return result

@app.get("/api/get_user_words")
async def get_words(session: SessionDep, 
                    payload: TokenPayload = Depends(auth_security.access_token_required)):
    query = select(models.Users_word).where(
        models.Users_word.user_id == int(payload.sub))
    result = await execute_query(query, session)
    return result

@app.get("/api/get_current_quiz_words")
async def get_current_quiz_words(session: SessionDep,
                                 payload: TokenPayload = Depends(auth_security.access_token_required)):
    users_words = await get_words(session, payload)
    #users_words[0]["Users_word"].origin
    length = len(users_words)
    if length < 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "Too few words!")
        
    quiz_questions = []
    
    for index, word in enumerate(users_words):
        correct_translation = word["Users_word"].translation
        other_words = users_words[:index] + users_words[index + 1:]
        incorrect_words = random.sample(other_words, k=3)
        incorrect_translations = [word["Users_word"].translation for word in incorrect_words]
        all_choices = incorrect_translations + [correct_translation]
        random.shuffle(all_choices)
        
        quiz_questions.append({
            "word_id": word["Users_word"].id,
            "english_word": word["Users_word"].origin,
            "correct_answer": correct_translation,
            "choices": all_choices
        })
    
    random.shuffle(quiz_questions) 
    return quiz_questions
 
# @app.post("/drop")
# async def drop():
#     async with engine.begin () as conn:
#         await conn.execute(text("DROP TABLE users_words CASCADE"))
#         await conn.execute(text("DROP TABLE users CASCADE"))
        
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)