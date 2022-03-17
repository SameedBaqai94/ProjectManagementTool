from xxlimited import new
from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
app=FastAPI()


#Database Connection
while True:
    try:
        conn=psycopg2.connect(host='127.0.0.1',database='fastapi',user='postgres',password='Shadow_12',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Database connection successfull!')
        break
    except Exception as err:
        print(f'Database connection failed, {err}')
        time.sleep(2)

class Post(BaseModel):
    title:str
    content:str
    published:bool=True

my_posts=[{"title":"title of post 1","content":"content for post 1","id":1},{"title":"Favourite Food","content":"Pizza","id":2}]

def find_id(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        
@app.get('/')
def root():
    return {'message':'welcome to api'}

@app.get('/posts')
def root(db:Session = Depends(get_db)):
    post=db.query(models.Post).all()
    return{"data":post}

@app.get('/posts/{id}',status_code=status.HTTP_200_OK)
def get_post(id:int,db:Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    #post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail":post}


@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db:Session = Depends(get_db)):
    #cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    #new_post=cursor.fetchone()
    #conn.commit()
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return({'Data':new_post})

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id)))

    delete_post=cursor.fetchone()
    conn.commit()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put('/posts/{id}')
def update_post(id:int,post:Post,status_code=status.HTTP_204_NO_CONTENT):
    cursor.execute("""UPDATE posts SET title= %s, content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
   
    return {"data":updated_post}


