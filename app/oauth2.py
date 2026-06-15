"""
This module is responsible for validating User sessions, by use of tokens.
- This ensures users are login and assign a valid token.
- This is then used for session validation over various API request to prove
    - who the user is 

-- create_access_token: 
    - Makes a copy of the input dictionary
    - Calculate expiration time
    - Add it to payload
    - Encode and signs the token using jwt.encode()
    - sign it with secret key and a specific algorithm.
    - Hence ensuring tokens can`t be tempered with.

-- verify_access_token:
    - This function validates access token, extract user credentials
        and return structured info about user, else exceptions.
    - It decodes the recieved data using the secret key and algorithm
    - Ensures token has not been tempered with.
    - Also checks expiration.
    - Structure the validated datat using pydantic

"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expiration_time
ALGORITHM = settings.algorithm


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jws = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jws


def verify_access_token(token: str, credentials_exceptions):
    """
    - credentials_exceptions arg define some meta rules about our token
    """
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        
        id: str = payload.get("user_id")
        print(id)
        print(type(id))
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exceptions
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """"
    It validates token and gets the current user from db
    """
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-AUthenticate": "Bearer"}
        )

    token = verify_access_token(token, credentials_exceptions)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user