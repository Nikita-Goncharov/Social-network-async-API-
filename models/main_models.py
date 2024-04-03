from datetime import date

from sqlalchemy import ForeignKey, String, Date, Text, select, update, delete, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession


class Base(AsyncAttrs, DeclarativeBase):

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    async def save(self):
        pass


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)

    profile: Mapped[int] = mapped_column(ForeignKey("profile.id"))


class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(250))
    education: Mapped[str] = mapped_column(String(250))
    web_site: Mapped[str] = mapped_column(String(250))
    country: Mapped[str] = mapped_column(String(250))
    city: Mapped[str] = mapped_column(String(250))
    birth_date: Mapped[date]
    created: Mapped[date] = mapped_column(Date(), default=date.today())
    followed: Mapped[bool]

    user: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique=True,  # if without unique, then will relation many-to-one, now it is one-to-one
        nullable=True  # nullable because first of all we create profile, and then user
    )

    posts: Mapped[Post] = relationship()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(250))
    password_hash: Mapped[str] = mapped_column(String(300))

    profile: Mapped[Profile] = relationship()
