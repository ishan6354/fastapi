from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# Declares the OAuth2 “password” flow for FastAPI’s dependency system.
# FastAPI will extract the token from the Authorization: Bearer <token> header and pass it into dependencies that declare Depends(oauth2_scheme). 
# tokenUrl='login' is the endpoint clients call to obtain tokens.


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

        #schemas.TokenData is a Pydantic model that wraps the claims in a typed object.
        #class TokenData(BaseModel):
        #    id: Optional[int] = None

    except JWTError:
        raise credentials_exception
    return token_data


# Depends is FastAPI’s dependency‑injection helper: it declares a callable (function/class) that FastAPI will run 
# and inject into your path operation or other dependencies, 
# letting you share logic like DB sessions, auth checks, and common parameters without repeating code. 
# Use Depends(...) to request a dependency; FastAPI resolves, caches, and tears it down per request. 


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):


    #Depends(oauth2_scheme) tells FastAPI to call the oauth2_scheme dependency for you and inject its return value into the parameter.
    #In this specific case oauth2_scheme is an instance of OAuth2PasswordBearer, a callable that extracts the bearer token from the incoming HTTP request and returns it as a string


    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.get(models.User, token.id)
    return user