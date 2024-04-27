from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from ..database import get_db, engine
from .. import models
from .. import schema
from .. import oauth2



router = APIRouter(
    prefix= '/posts',
    tags=['Post']
)



@router.get('', response_model=list[schema.PostPublic])  
async def get_posts(db:AsyncSession = Depends(get_db), current_user: schema.User = Depends(oauth2.get_current_user),
                    limit: int = 10, search: Optional[str] = ''):
    
    select_query = select(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                        models.Vote.post_id == models.Post.id,
                                        isouter=True).group_by(models.Post.id).where(models.Post.title.contains(search)).limit(limit)
    
    posts = await db.execute(select_query)
    return posts.all()

@router.post('', status_code=201, response_model= schema.Post)
async def create_post(post: schema.PostCreate, db:AsyncSession = Depends(get_db),
                       current_user: schema.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model= schema.PostPublic)
async def get_post(id:int, db:AsyncSession = Depends(get_db),
                    current_user: schema.User = Depends(oauth2.get_current_user)):
    select_query = select(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                        models.Vote.post_id == models.Post.id,
                                        isouter=True).group_by(models.Post.id).having(models.Post.id == id)
    
    result = await db.execute(select_query)
    post = result.scalar_one_or_none()
    if post:
        return post
    raise HTTPException(status_code=404,
                        detail=f'Post with ID {id} not found')
    

@router.delete('/{id}',status_code=204)
async def delete_post(id:int,db:AsyncSession = Depends(get_db),
                        current_user: schema.User = Depends(oauth2.get_current_user)):
    select_query = select(models.Post).where(models.Post.id == id)
    result = await db.execute(select_query)
    post = result.scalar_one()

    if post:
        if post.user_id == current_user.id:
            await db.delete(post.scalar_one_or_none())
            await db.commit()
            return Response(status_code=204)
        raise HTTPException(status_code=403, detail=f'Not authorized to perform this action')
    
    raise HTTPException(status_code=404,
                        detail=f'Post with ID {id} not found')

@router.put('/{id}', status_code=200)
async def update_post(id:int, post:schema.PostCreate, db:AsyncSession = Depends(get_db)
                       ,current_user: schema.User = Depends(oauth2.get_current_user)):
    select_query = select(models.Post).where(models.Post.id == id)
    result = await db.execute(select_query)
    post_query = result.scalar_one_or_none()
    if post_query:
        if post_query.user_id == current_user.id:
            db.add(post.model_dump())
            await db.commit()
            return post
        raise HTTPException(status_code=403, detail=f'Not authorized to perform this action')
    raise HTTPException(status_code=404,
                        detail=f'Post with ID {id} not found')
