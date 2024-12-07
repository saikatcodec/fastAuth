from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated, Any
from starlette import status
from sqlmodel import Session, select, col

from app import db
from app import models
from app.config import setting
from app.deps import confirm_token, current_user, send_message, generate_confirmation_token
from app.utils import hashed_pass, verify_pass, create_access_token
from app.templates.account_verification import get_account_verification_template
from app.templates.reset_templates import get_reset_password_email_template

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
    
    verification_token = generate_confirmation_token(user.email)
    link = setting.DOMAIN + f'/auth/verify-user/{verification_token}'
    subject =  'Welcome to FastAuth'
    body = get_account_verification_template(verification_link=link)
    await send_message(subject=subject, body=body, email=user.email)
    
    return  user_db


@router.get('/verify-user/{token}')
async def verify_user(token: str, session: sessionDp):
    email = confirm_token(token)
    
    statement = select(models.User).where(col(models.User.email) == email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {'message': 'User verified successfully'}

@router.post('/reset-password')
async def reset_password(email_data: models.PasswordResetReq):
    token = generate_confirmation_token(email_data.email)
    
    link = setting.DOMAIN + f'/auth/reset-password-confirm/{token}'
    subject =  'Password Reset'
    body = get_reset_password_email_template(link)
    await send_message(subject=subject, body=body, email=email_data.email)
    
    return {'message': 'Password reset link sent successfully'} 

@router.post('/reset-password-confirm/{token}')
async def reset_password_confirm(token: str, data: models.PasswordResetConfirm, session: sessionDp):
    email = confirm_token(token)
    
    statement = select(models.User).where(col(models.User.email) == email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    user.hashed_password = hashed_pass(data.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {'message': 'Password reset successfully'}