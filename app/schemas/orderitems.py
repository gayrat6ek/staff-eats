from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from .groups import GroupsGet, GroupNameGet



class OrderItemsGet(BaseModel):
    amount:int
    group:Optional[GroupNameGet] = None
    class Config:
        orm_mode = True