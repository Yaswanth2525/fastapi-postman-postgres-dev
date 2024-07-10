from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database,schemas,models
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
# Algorithm
# Expiration time - infinity means login forever

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    
    
def verify_access_token(token:str,credentials_exception):
    try:
        # print(token)
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        user_id:str = payload.get("user_id")
        # present or not
        if user_id is None:
            raise credentials_exception
        # validation
        token_data = schemas.TokenData(id=str(user_id))
    except JWTError as e:
        # print("error",e)
        raise credentials_exception
    # print(token_data)
    return token_data
        
def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    print("current_user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials",
        headers = {"WWW-Authenticate":"Bearer"}
    )
    
    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    
    return user
    































