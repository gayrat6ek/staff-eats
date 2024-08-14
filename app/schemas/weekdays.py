from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .menus import MenusGet
from app.schemas.files import FilesGet

class WeekdaysCreate(BaseModel):
    name: str
    description: Optional[str]=None
    is_active: Optional[int]=None
    file: Optional[str]=None
    meals: Optional[list[int]]=None
    class Config:
        orm_mode = True

class WeekdaysUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    file : Optional[str]=None
    meals: Optional[list[int]]=None
    id:int
    class Config:
        orm_mode = True


class WeekdaysGet(BaseModel):
    id:int
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    file: Optional[list[FilesGet]] = None
    class Config:
        orm_mode = True


class WeekdaysMenu(BaseModel):
    id:int
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    menu: Optional[list[MenusGet]] = None
    file : Optional[list[FilesGet]]=None
    class Config:
        orm_mode = True