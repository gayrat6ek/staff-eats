from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
)
from app.utils.utils import file_name_generator
from app.routes.depth import get_db, get_current_user
from app.schemas import users as user_sch


file_router = APIRouter()


@file_router.post("/file/upload",)
async def read_files(
    file:UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    file_path = f"files/{file_name_generator()}{file.filename}"
    with open(file_path, "wb") as buffer:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            buffer.write(chunk)
    return {"file_name": file_path}

