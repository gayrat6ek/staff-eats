from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class RatingsCreate(BaseModel):
    rating: int
    meal_id: int
    client_id: int
    class Config:
        orm_mode = True


class RatingsGet(BaseModel):
    rating: int
    meal_id: int
    client_id: int
    class Config:
        orm_mode = True

