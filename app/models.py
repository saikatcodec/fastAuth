import uuid
from sqlmodel import Field, SQLModel
from pydantic import EmailStr

class UserBase(SQLModel):
    name: str | None = Field(default=False, max_length=255)
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(unique=True)
    
class User(UserBase, table=True):
    password: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True, primary_key=True)
    
class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    username: str