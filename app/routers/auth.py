from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any
from starlette import status
from sqlmodel import Session, select, col
from fastapi.security import OAuth2PasswordRequestForm

from app import db
from app import models
from app.deps import current_user
from app.utils import hashed_pass, verify_pass, create_access_token

router = APIRouter()


sessionDp = Annotated[Session, Depends(db.get_db)]

@router.post('/token')
async def login(session: sessionDp, user: models.UserLogin) -> models.Token:
    statement = select(models.User).where(col(models.User.email) == user.email)
    user_found = session.exec(statement).first()
    
    if not user_found:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Credentials')
    
    if not verify_pass(user.password, user_found.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong Credentials')
    
    token = create_access_token({'sub': str(user_found.id), 'email': user_found.email})
    
    return models.Token(token=token, token_type='Bearer')


@router.get('/validate', response_model=models.UserPublic)
async def get_user(user: Annotated[Any, Depends(current_user)]):
    return user
    

@router.post('/register', response_model=models.UserPublic)
async def register(user: models.UserCreate, session: sessionDp):
    statement = select(models.User).where(col(models.User.email) == user.email)
    user_found = session.exec(statement).first()
    
    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')
    
    user_db = models.User(
        name=user.name,
        email=user.email,
        username=user.username,
        hashed_password=hashed_pass(user.password)
    )
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    
    return user_db