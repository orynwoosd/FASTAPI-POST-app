from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = ""
ACCESS_TOKEN_EXPIRES_MINUTES = 60 
ALGORITHM = "HS256"


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