from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class FilesGet(BaseModel):
    id:int
    url : str
    class Config:
        orm_mode = True



class FilesDelete(BaseModel):
    id:int

