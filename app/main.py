
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
from passlib.context import CryptContext
from . import utils
from .routers import auth, post, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


  

while True:
    try:
        conn = psycopg2.connect(
            host="localhost", database="fastapi", 
            user="postgres", password="THhjn684&_",
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