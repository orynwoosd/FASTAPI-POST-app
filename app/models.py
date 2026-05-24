from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql.sqltypes import TIMESTAMP


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