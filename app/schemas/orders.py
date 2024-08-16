from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .orderitems import OrderItemsGet
from .departments import DepartmentsGetAll

class OrdersGet(BaseModel):
    id: int
    client_id: int
    orderitem: Optional[list[OrderItemsGet]] = None
    department: Optional[DepartmentsGetAll] = None
    created_at: Optional[datetime] = None
    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    client_id: int
    orderitems: Optional[list[Dict]] = None
    department_id: Optional[int] = None
    class Config:
        orm_mode = True


