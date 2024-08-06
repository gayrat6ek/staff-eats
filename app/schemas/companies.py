from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID

class CompaniesCreate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    class Config:
        orm_mode = True

class CompaniesUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    id:int
    class Config:
        orm_mode = True

class CompaniesGet(BaseModel):
    id:int
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    class Config:
        orm_mode = True
