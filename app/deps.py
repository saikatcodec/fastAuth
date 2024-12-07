import jwt
from typing import Annotated, Dict
from fastapi import Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from starlette import status

from app import db
from app.config import setting
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