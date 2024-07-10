from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# my_posts = [
#     {"title":"title of post 1",
#     "content":"content of post 1",
#     "id":1},
#     {"title":"favourite fooods",
#     "content":"I like pizza",
#     "id":2}
# ]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
    
# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p["id"] == id:
#             return i
        


@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int = 5,skip:int = 0,search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # post = cursor.fetchall()
    # return {"data":post}
    # # post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # print(limit)
    # post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    
    # # return {"data":post}
    return posts
    # return {"data" :my_posts }

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print("create_posts")
    # # post_dict = post.model_dump()
    # # post_dict['id']=randrange(0,10000000)
    # # my_posts.append(post_dict)
    # # return {"data ":post_dict}
    # # sql stat injection attack
    # # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ({post.title},{post.content},{post.published})") - hacker may modified with help typing sql stat in title
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":new_post}
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # # # return {'data':new_post}
    return new_post
# title : str , content : str
# check for similar path parameter like(posts/{id} and posts/latest) check order
# here comes order if this were present below post/{id} the output will detail:null
@router.get("/latest")
def get_latest():
    post = my_posts[len(my_posts)-1]
    return {"detail":post}
    
 
@router.get("/{id}",response_model=schemas.PostOut)
# if id is not integer pydantic will issue error of type dictionary
def get_post(id:int,response:Response,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # # print(id)
    # # post = find_post(id)
    # # if not post:
    #     # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    # #     # response.status_code = status.HTTP_404_NOT_FOUND
    # #     # return {'message':f"post with id :{id} was not found"}
    # # return {"post_detail" : post}
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    # return {"post_detail":post}
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True
    ).group_by(
        models.Post.id
    ).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
    # # # # return {"post ":post}
    # if post.owner_id != current_user.id :
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorised to perform requested action")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # # # deleting post
    # # # find index in the array that has Id as id
    # # # my_posts.pop(index)
    # # index = find_index_post(id)
    # # if index == None:
    # #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    # # my_posts.pop(index)
    # # # return {'message':"post successfully deleted"}
    # # return Response(status_code=status.HTTP_204_NO_CONTENT)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post: schemas.PostCreate,db : Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # # index = find_index_post(id)
    # # if index == None:
    # #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    # # post_dict=post.model_dump()
    # # post_dict['id'] = id
    # # my_posts[index] = post_dict
    # # return {'data':post_dict}
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s  RETURNING *""",(post.title,post.content,post.published,str(id)))
    # upd_post = cursor.fetchone()
    # if upd_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    # conn.commit()
    # return {'data':upd_post}
    updpost_query = db.query(models.Post).filter(models.Post.id==id)
    
    updpost = updpost_query.first()
    
    if updpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exit")
    
    
    if updpost.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorised to perform requested action")
    
    
    # post.update({'title':"new title",'content':"new content"},synchronize_session = False)
    updpost_query.update(post.model_dump(),synchronize_session = False)
    db.commit()
    # # # # return {'data':updpost.first()}
    return updpost_query.first()
