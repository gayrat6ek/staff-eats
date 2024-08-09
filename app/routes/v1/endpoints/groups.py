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

from app.routes.depth import get_db, get_current_user
from app.schemas import users as user_sch
from app.crud import groups as group_crud
from app.schemas import groups as group_sch


group_router = APIRouter()


@group_router.get(
    "/groups",
    response_model=Page[group_sch.GroupsGet],
    response_model_exclude_none=True,
)
async def get_groups(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    groups = group_crud.get_groups(db=db,id=id)
    return paginate(groups)


@group_router.post(
    "/groups",
    response_model=group_sch.GroupsGet,
    response_model_exclude_none=True,
)
async def create_group(
    form_data: group_sch.GroupsCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return group_crud.create_group(db=db, form_data=form_data)


@group_router.put(
    "/groups",
    response_model=group_sch.GroupsGet,
    response_model_exclude_none=True,
)
async def update_group(
    form_data: group_sch.GroupsUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return group_crud.update_group(db=db, form_data=form_data)


@group_router.get(
    "/group/{id}",
    response_model=group_sch.GroupsGet,
)
async def get_one_group(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return group_crud.get_one_group(db=db, id=id)

