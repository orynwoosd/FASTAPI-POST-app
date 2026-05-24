from pwdlib import PasswordHash
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


ALGORITHM = "HS256"


password_harsh = PasswordHash.recommended()


def hash_password(plain_pass):
    return password_harsh.hash(plain_pass)

def verify_password(plain_pass, hashed_pass):
    print(password_harsh.verify(plain_pass, hashed_pass))
    return password_harsh.verify(plain_pass, hashed_pass)

