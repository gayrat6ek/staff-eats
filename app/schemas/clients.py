from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .departments import DepartmentsGetAll



class ClientsGet(BaseModel):
    id:int
    name:Optional[str] = None
    username:Optional[str] = None
    telegram_id:Optional[str] = None
    is_active:Optional[bool] = None
    department_id:Optional[int] = None
    department : Optional[DepartmentsGetAll] = None
    class Config:
        orm_mode = True


class ClientsCreate(BaseModel):
    name:Optional[str] = None
    username:Optional[str] = None
    telegram_id:str
    is_active:Optional[int] = None
    department_id:int
    class Config:
        orm_mode = True


class ClientsUpdate(BaseModel):
    name:Optional[str] = None
    username:Optional[str] = None
    telegram_id:Optional[str] = None
    is_active:Optional[int] = None
    department_id:Optional[int] = None
    id:int
    class Config:
        orm_mode = True


class Logout(BaseModel):
    telegram_id:str
    class Config:
        orm_mode = True