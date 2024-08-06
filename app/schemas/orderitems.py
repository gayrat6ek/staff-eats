from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .meals import GetMeals



class OrderItemsGet(BaseModel):
    order_id:int
    amount:int
    meal_id:int
    meal:Optional[GetMeals] = None
    class Config:
        orm_mode = True