from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from . import schema, database, models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

async def create_access_token(data: dict):
    to_encode = data.copy() 

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_acces_token(token: str, credential_exception):
    try:

        payload = jwt.decode(token=token, key= SECRET_KEY, algorithms=ALGORITHM)

        id: str = str(payload.get("user_id"))

        if id:
            print(id)
            return schema.TokenData(id=id)
        raise credential_exception
    except JWTError:
        raise credential_exception
    
async def get_current_user(token: str, str = Depends(oauth2_scheme),
                     db: AsyncSession = Depends(database.get_db)):
    
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail='could not validate credentials',
                                          headers={'WWW-Authenticate':'Bearer'})
    
    token_data = await verify_acces_token(token, credentials_exception)
    select_query = select(models.User).where(models.User.id == int(token_data.id))
    user = await db.execute(select_query)
    return user.scalar_one()