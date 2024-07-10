from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from .. import database,schemas,models,utils,oauth2


router = APIRouter(tags = ['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(usr_crd:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session = Depends(database.get_db)):
    # {
    #     "username":"asdf",
    #     "password","alsdfj"
    # }
    user = db.query(models.User).filter(models.User.email == usr_crd.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verify(usr_crd.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    # return token
    return {"access_token" : access_token,"token_type":"bearer" }
    
    












