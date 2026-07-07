"""
OverView:
This file defines all SQLAlchemy ORM models and represents tables in the db
In this file each class corresponds to a table in the database, and specifies;
- The table structure (columns, data types, constraints)
- Relations between tables, (e.g., ForeingKeys, Index)
- Model level and database level validation rules.
- This file is now 


- Linking it with alembic allows us to auto create tables.
    - with this alembic can import our models and analyze them.
    - It can figure out what columns are missing and fill them in.
    - It can fill constraints to and also create new tables 
    - This is all done by reading are models
"""


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
    # The just help us refrence tables with each other for ease of communication
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
    # phone_number: Mapped[str] = mapped_column(String(100))



class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)