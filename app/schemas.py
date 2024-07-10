from pydantic import BaseModel,EmailStr, conint,Field
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

# class Post(BaseModel):
#     title: str
#     content: str
#     published : bool = True
    
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published : bool = True

# # adding attribute that can be modified not anything else
# # like only published changeble means ,remove 16,17 lines
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published : bool

class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

   
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        form_attributes = True

 
class Post(PostBase):
    id:int
    created_at:datetime
    owner_id : int
    owner : UserOut
    
    class Config:
        from_attributes = True
      

class PostOut(BaseModel):
    Post : Post
    votes : int
    
    class Config:
        from_attributes = True
       
class UserCreate(BaseModel):
    email:EmailStr
    password:str
 

class UserLogin(BaseModel):
    email:EmailStr
    password:str

        
        
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : str
    
VoteInt=conint(le=1)

class Vote(BaseModel):
    post_id : int
    dir : Annotated[int, Field(strict=True, le=1)]

    



    
















    