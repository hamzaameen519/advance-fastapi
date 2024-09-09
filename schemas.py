from pydantic import BaseModel # type: ignore
from typing import Optional
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int
    is_active: bool

class UserUpdate(BaseModel):
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    is_active: Optional[bool] = None
    class Config:
        orm_mode = True
