from pydantic import BaseModel # type: ignore

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
