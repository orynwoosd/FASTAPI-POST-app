from pydantic import BaseModel, EmailStr, Field
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

    class Config:
        orm_mode = True


class Post(PostBase):
    
    id: int
    created_at: datetime
    user_id: int
    owner: UserOut = Field(alias="author")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

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

