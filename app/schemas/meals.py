from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .files import FilesGet

class CreateMeals(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    price: Optional[float] = None
    group_id: int

    class Config:
        orm_mode = True


class UpdateMeals(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    group_id: Optional[int] = None
    price: Optional[float] = None
    id: int

    class Config:
        orm_mode = True


class GetMeals(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None
    group_id: Optional[int] = None
    price: Optional[float] = None
    class Config:
        orm_mode = True