from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db, engine
from .. import models
from .. import schema
from .. import oauth2



router = APIRouter(
    prefix= '/vote',
    tags=['Vote']
)

@router.post('', status_code=201)
async def vote(vote: schema.Vote, db: AsyncSession = Depends(get_db),
               current_user : schema.User = Depends(oauth2.get_current_user)):
    
    select_query = select(models.Post).filter(models.Post.id == vote.post_id)
    result = await db.execute(select_query)

    if not await result.scalar_one_or_none():
        raise HTTPException(status_code=404,details='Post not found')
    
    vote_query = select(models.Vote).where(models.Vote.post_id == vote.post_id,
                                               models.Vote.user_id == current_user.id)
    result = await db.execute(vote_query)
    found_vote = result.scalar_one_or_none()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, 
                                detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(user_id=current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        await db.commit()
        return {'message':'vote successfully added'}
    
    else:
        if found_vote:
            db.delete(found_vote)
            await db.commit()
            return {'message':'successfully deleted vote'}
        raise HTTPException(status_code=404, detail=f'Vote doesnot exist')
