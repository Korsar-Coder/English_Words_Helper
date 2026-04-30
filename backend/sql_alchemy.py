from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, ARRAY, UniqueConstraint
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
    origin = Column(String, unique=True)
    translation = Column(ARRAY(String))

class Users_word(Base):
    __tablename__ = "users_words"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words_info.id"))
    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name='unique_word_user'),
    )

Base.metadata.create_all(engine)
# test_user = User(name= "John")
# test_words = [Word_Info(origin= "Guitar", translation= ["Гитара"]),
#                Word_Info(origin= "Programmer", translation= ["Программист"])]
# session.add_all([test_user, *test_words])
# session.commit()

words = session.query(Word_Info).all()
print(words[1].translation)