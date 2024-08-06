from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .meals import GetMeals


class MenusCreate(BaseModel):
    meal_id:int
    weekday_id:int
    is_active: Optional[int] = None
    class Config:
        orm_mode = True


class MenusDelete(BaseModel):
    id:int


class MenusGet(BaseModel):
    id:int
    meal_id:int
    weekday_id:int
    meal : Optional[GetMeals] = None
    class Config:
        orm_mode = True
