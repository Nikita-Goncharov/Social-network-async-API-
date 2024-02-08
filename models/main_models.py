from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    education: Mapped[str]
    web_site: Mapped[str]
    birth_date: Mapped[date]
    user: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,  # if without unique, then will relation many-to-one, now it is one-to-one
        nullable=True  # nullable because first of all we create profile, and then user
    )


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    img: Mapped[str]
    status: Mapped[str]
    followed: Mapped[bool]
    country: Mapped[str]
    city: Mapped[str]
    profile: Mapped[Profile] = relationship()

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

