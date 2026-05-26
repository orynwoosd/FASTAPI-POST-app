"""
- Never return and HTTP exception class,rather raise it, due to serialization problems.

"""


from .. import models, schemas, utils, oauth2

from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from psycopg2.extras import RealDictCursor
from ..database import get_db
from sqlalchemy.orm import Session, joinedload
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_all_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursur.execute(""" SELECT * FROM posts """)
    # posts = cursur.fetchall()

    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id ).all()
    posts = db.query(
        models.Post
        ).options(joinedload(models.Post.author)).all()

    return posts



@router.get("/{id}", response_model=schemas.Post)
def get_a_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursur.execute("""SELECT * FROM posts WHERE id = %s """, (str(item_id)))
    # post = cursur.fetchone()
    # if not post:
    #     return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    

    post = db.query(models.Post).options(joinedload(models.Post.author)).filter(models.Post.id == id).first()
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perfomr such action")
    
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    print(post)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Why is %s used here and not direct variable insertion., 1. sequel injection possible if F-string is used.
    # This can't be stored in variable directly, even with the RETURNING commad.
    # cursur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (posts.title, posts.content, posts.published))
    # new_post = cursur.fetchone()
    # conn.commit()
    # new_posts = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))

    # updated_post = cursur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() != None: 
        if post.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perfomr such action")
        
        post_query.update(updated_post.dict(), synchronize_session=False)

        db.commit()

        return post_query.first()
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursur.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id)))

    # deleted_post = cursur.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() != None: 

        if post.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize to perfomr such action")

        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id not found")


