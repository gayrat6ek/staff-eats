from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID



class DepartmentsCreate(BaseModel):
    name: str
    description: Optional[str]=None
    is_active: Optional[int]=None
    company_id : int
    password: str
    class Config:
        orm_mode = True



class DepartmentsUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None
    is_active: Optional[int]=None
    password: Optional[str]=None
    id:int
    class Config:
        orm_mode = True



class DepartmentsGet(BaseModel):
    id:int
    name: Optional[str]=None
    description: Optional[str]=None
    company_id: Optional[int]=None
    password: Optional[str]=None
    class Config:
        orm_mode = True