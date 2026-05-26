from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False
        )
    title: Mapped[str] = mapped_column(
        String(50), nullable=False
        )
    content: Mapped[str] = mapped_column(
        String(255), nullable=False)
    published: Mapped[bool] = mapped_column(
        Boolean, server_default="TRUE", nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships are completely independent of the database, all logic works without them.
    # The just help us refrence tables with each orther for ease of communication
    author: Mapped["User"] = relationship(back_populates="posts")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )

    password: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
    TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )

    posts: Mapped[List["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")