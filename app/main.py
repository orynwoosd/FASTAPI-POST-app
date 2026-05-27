"""

"""
from fastapi import FastAPI, Depends

import time
from . import models
from .database import engine
from . import models 
from typing import List
from .routers import auth, post, user
from .config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


  


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)