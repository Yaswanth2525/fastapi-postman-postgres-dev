# order of execution of functions is from top to bottom
# if there is any similar kind post

from fastapi import FastAPI,Depends
# from fastapi.params import Body
# from pydantic import BaseModel
#pydantic does the error job and return status code
# from random import randrange

from sqlalchemy.orm import Session
from .import models
from .database import engine,get_db
from .routers import post,user,auth,vote
# from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# create all models
models.Base.metadata.create_all(bind=engine)

# run command - 
    # activate.bat in scritps
    # uvicorn main:app  #  single time run at compile time
    # uvicorn main:app --reload # reload until exit command 
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# all CRUD OPERATIONS
# request Get method url: "/"
# FIFO functions if same function_name
# decorative(@)_(api_name).(http request method)(url)
@app.get("/")
# what doest url do by root functions 
async def root():
    return {"message": "hello world"}

@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}






















    