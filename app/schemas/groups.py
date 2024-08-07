from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .meals import GetMeals


class GroupsCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None

    class Config:
        orm_mode = True


class GroupsUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    id: int

    class Config:
        orm_mode = True


class GroupsGet(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    meal: Optional[list[GetMeals]] = None

    class Config:
        orm_mode = True



class GroupNameGet(BaseModel):
    id: int
    name: Optional[str] = None

    class Config:
        orm_mode = True
