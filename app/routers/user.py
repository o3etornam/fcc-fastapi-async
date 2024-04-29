from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from .. import models
from .. import schema
from .. import utlis



router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)



@router.post('', status_code=201, response_model=schema.User)
async def create_user(user: schema.UserCreate, db:AsyncSession = Depends(get_db)):
    user.password = await utlis.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
    

@router.get('', response_model= List[schema.User])  
async def get_users(db:AsyncSession = Depends(get_db)):
    select_query = select(models.User)
    users = await db.execute(select_query)
    #users = db.query(models.User).all()
    return users.scalars().all()

@router.get('/{id}', response_model= schema.User)
async def get_user(id: int, db:AsyncSession = Depends(get_db)):
    select_query = select(models.User).where(models.User.id == id)
    result = await db.execute(select_query)
    user = result.scalar_one_or_none()
    #user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    raise HTTPException(status_code=404, detail=f'User with id {id} doesn\'t exsit')