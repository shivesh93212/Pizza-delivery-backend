
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username:str
    email:str
    password:str
    is_staff:bool=False
    is_active:bool=False

    class Config:
        orm_mode=True
        schema_extra={
            "example":{ 
            "username":"shivesh",
            "email":"shiveshpatel853@gmail.com",
            "password":"password",
            "is_staff":False,
            "is_active":True
            }
        }

class UserLogin(BaseModel):
    email:str
    password:str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_staff: bool
    is_active: bool

    class Config:
        orm_mode = True
