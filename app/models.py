import uuid
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr

class UserBase(SQLModel):
    name: str | None = Field(default=False, max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True)
    
class UserCreate(UserBase):
    password: str
    
class User(UserBase, table=True):
    __tablename__ = 'users'
    hashed_password: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, primary_key=True)
    
class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    
class UserLogin(SQLModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    token: str
    token_type: str
    
class TokenData(BaseModel):
    sub: uuid.UUID
    email: EmailStr