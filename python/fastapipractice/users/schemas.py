from typing import List

from pydantic import BaseModel


class UserBase(BaseModel):
    sns_id: str


class UserCreate(UserBase):
    email: str
    name: str
    access_token: str
    refresh_token: str


class User(UserBase):
    id: int
    sns_id = str
    is_active: bool

    class Config:
        orm_mode = True
