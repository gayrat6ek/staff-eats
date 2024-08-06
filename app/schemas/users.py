from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from app.schemas.files import FilesGet



class UserCreate(BaseModel):
    username: str
    surname:Optional[str] = None
    name:Optional[str] = None
    file : Optional[str] = None
    password: str
    is_active: Optional[int]=None
    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str]=None
    surname: Optional[str]=None
    name: Optional[str]=None
    file : Optional[str] = None
    password: Optional[str]=None
    is_active: Optional[int]=None
    id:int
    class Config:
        orm_mode = True

class UserGet(BaseModel):
    id:int
    username: Optional[str]=None
    surname: Optional[str]=None
    name: Optional[str]=None
    is_active: Optional[int]=None
    file :Optional[list[FilesGet]]=None
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username:str
    password:str