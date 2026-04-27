from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import json

with open("config.json", "r") as file:
    config = json.load(file)

Base = declarative_base()
engine = create_engine(f"postgresql://postgres:{config["password"]}@localhost/{config["database"]}")
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Word_Info(Base):
    __tablename__ = "words_info"
    id = Column(Integer, primary_key=True)
    origin = Column(String)
    translation = Column(String)

class Users_word(Base):
    __tablename__ = "users_words"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words_info.id"))

Base.metadata.create_all(engine)