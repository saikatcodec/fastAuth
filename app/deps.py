import jwt
from typing import Annotated, Dict
from fastapi import Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from starlette import status
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

from app import db
from app.config import setting
from app.mail import mail, create_message
from app.models import Token, TokenData, User


sessionDp = Annotated[Session, Depends(db.get_db)]
oauth_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')
tokenDp = Annotated[Token, Depends(oauth_schema)]

def current_user(session: sessionDp, token: tokenDp) -> Dict:
    try:
        payload = jwt.decode(token, setting.JWT_KEY, algorithms=setting.ALGORITHM)
        
        token_data = TokenData(**payload)
        
    except (InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
        
    user = session.get(User, token_data.sub)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user

async def send_message(subject: str, body: str, email: str):
    message = create_message([email], subject, body)
    
    await mail.send_message(message)



serializer = URLSafeTimedSerializer(secret_key=setting.SECRET_KEY, salt=setting.SALT)

def generate_confirmation_token(email: str) -> str:
    return serializer.dumps(email)

def confirm_token(token: str, expiration=3600) -> str:
    try:
        email = serializer.loads(token, max_age=expiration)
        return email
    except SignatureExpired as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token expired')