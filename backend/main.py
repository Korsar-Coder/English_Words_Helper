import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import engine, Base, get_session
from typing import Annotated
import models 
from pydantic import BaseModel, Field 
from security import get_password_hash

app = FastAPI()

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

@app.post("/add_user")
async def add_user(data: UserSchema, session: SessionDep):
    user_in_db = UserAddSchema.hash_password(name= data.name,
                                             raw_password=data.raw_password)
    new_user = models.User(**user_in_db.model_dump())
    session.add(new_user)
    await session.commit()
    return {"Champion" : True}

@app.get("/get_user{name}")
async def get_user(data: str, session: SessionDep):
    query = select(models.User).where(models.User.name == data)
    result = await session.execute(query)
    return result.scalars().all()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
