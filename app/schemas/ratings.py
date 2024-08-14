from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from app.schemas.meals import GetMeals
from app.schemas.clients import ClientsGet


class RatingsCreate(BaseModel):
    rating: Optional[int] = None
    meal_id: int
    client_id: int
    comment: Optional[str] = None
    class Config:
        orm_mode = True


class RatingsGet(BaseModel):
    rating: Optional[int] = None
    meal_id: int
    meal: Optional[GetMeals] = None
    client_id: int
    client: Optional[ClientsGet] = None
    comment: Optional[str] = None
    class Config:
        orm_mode = True

