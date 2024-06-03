from datetime import date, datetime

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Dialog(Base):
    __tablename__ = "dialog"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_profile: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    second_profile: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())


class Message(Base):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(300))
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    owner: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    dialog: Mapped[int] = mapped_column(ForeignKey("dialog.id"))


class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    profile: Mapped[int] = mapped_column(ForeignKey("profile.id"))


class FollowProfile(Base):
    __tablename__ = "follow_profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    follower: Mapped[int] = mapped_column(ForeignKey("profile.id"))
    who_are_followed: Mapped[int] = mapped_column(ForeignKey("profile.id"))


class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    img: Mapped[str] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(250))
    education: Mapped[str] = mapped_column(String(250))
    web_site: Mapped[str] = mapped_column(String(250))
    country: Mapped[str] = mapped_column(String(250))
    city: Mapped[str] = mapped_column(String(250))
    birth_date: Mapped[datetime] = mapped_column(DateTime(), nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())

    user: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique=True,  # if without unique, then will relation many-to-one, now it is one-to-one
        nullable=True  # nullable because first of all we create profile, and then user
    )
    user_obj: Mapped["User"] = relationship(back_populates="profile", lazy="joined")

    posts: Mapped[Post] = relationship()


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(250), unique=True)
    token: Mapped[str] = mapped_column(String(300), default="")
    password_hash: Mapped[str] = mapped_column(String(300))

    profile: Mapped[Profile] = relationship(back_populates="user_obj", lazy="joined")
