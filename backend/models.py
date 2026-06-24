from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    hashed_password: Mapped[str] = mapped_column()
    __table_args__ = (
        CheckConstraint("TRIM(username) <> ''", name="username_not_empty"),
    )
    
class Word_Info(Base):
    __tablename__ = "words_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    origin: Mapped[str] = mapped_column(unique=True)
    translation: Mapped[str] 

class Users_word(Base):
    __tablename__ = "users_words"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    word_id: Mapped[int] = mapped_column(ForeignKey("words_info.id"))

    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name="unique_word_user"),
    )