"""
- This file holds the pydantic models that define the structure, type hints
    and validation rules for data flowing through the application.
Key Validations;
- Request validations, which ensures incoming data, from API requests matches expected format.
- Response modeling, which defines structure of data the API returns to clients
- Data parsing, by converting raw JSON into python objects with correct data
- Error feedbacks, are cleean and easy to debug.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.types import conint
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class Post(PostBase):
    
    id: int
    created_at: datetime
    user_id: int
    author: UserOut 


    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True 
    )

class PostVote(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(
        orm=True,
        from_attributes=True,
        validate_by_name=True
        )

class UserCreate(BaseModel):
    email: EmailStr
    password: str




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    totken_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    disabled: bool

class UserInDB(BaseModel):
    hashed_password: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)