from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, main_config

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    __table_args__ = (
        CheckConstraint("TRIM(name) <> ''", name="username_not_empty"),
    )
    
# class Word_Info(Base):
#     __tablename__ = "words_info"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     origin: Mapped[str] = mapped_column()
#     translation: Mapped[str] 
#     __table_args__ = (
#         UniqueConstraint('origin', 'translation', name='origin_translation_unique'),
#     )
    
class Users_word(Base):
    __tablename__ = "users_words"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    origin: Mapped[str]
    translation: Mapped[str]
    __table_args__ = (
        UniqueConstraint("origin", "translation", name='origin_translation_unique'),
    )