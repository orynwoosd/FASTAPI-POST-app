
"""
OverView:
This file is the main powerhouse of the application and 
everything diverges from here to orther files. i.e., its the main
FASTAPI instance of this app.
It ensures database is avaibale before starting the application.

 - It sets up the database connection and initializes 
    all sqlalchemy modules
 - It also implements application routers.
    - the user, auth etc., for communicatinf with this routing files.
 - It implements a retry mechanism to ensure a wait and reconect
    between failures.
"""

from fastapi import FastAPI, status, HTTPException, Response, Depends
# from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models 
from . import schemas
from typing import List
# from passlib.context import CryptContext
from . import utils
from .routers import auth, post, user, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
  

while True:
    try:
        conn = psycopg2.connect(
            host="localhost", database=settings.database_name, 
            user="postgres", password=settings .database_password,
            cursor_factory=RealDictCursor
            )
        cursur = conn.cursor()
        print("databse connection was success")
        break
    except Exception as e:
        time.sleep(2) 
        print(e)
        print("connection databse failed")


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)