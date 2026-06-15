"""
- This module provide simple utils for harshing passwords.
- It converts passwords into irreversible harsh before storing them
- Also verifys if plain-text passwordsmatches what had been stored in base.
- Uses a  slow harshing algorithm (Argon) which thwarts brute-force attacks.

"""

from pwdlib import PasswordHash
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


ALGORITHM = "HS256"


password_harsh = PasswordHash.recommended()


def hash_password(plain_pass):
    return password_harsh.hash(plain_pass)

def verify_password(plain_pass, hashed_pass):
    # print(password_harsh.verify(plain_pass, hashed_pass))
    return password_harsh.verify(plain_pass, hashed_pass)

