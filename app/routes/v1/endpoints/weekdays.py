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
from app.schemas import weekdays as weekday_sch
from app.crud import weekdays as weekday_crud
from app.crud import files as file_crud


weekday_router = APIRouter()


@weekday_router.get(
    "/weekdays",
    response_model=Page[weekday_sch.WeekdaysGet],
    response_model_exclude_none=True,
)
async def get_weekdays(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    weekdays = weekday_crud.get_weekdays(db=db,id=id)
    return paginate(weekdays)

@weekday_router.post(
    "/weekdays",
    response_model=weekday_sch.WeekdaysGet,
    response_model_exclude_none=True,
)
async def create_weekdays(
    form_data: weekday_sch.WeekdaysCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query =  weekday_crud.create_weekday(db=db, form_data=form_data)
    if form_data.file is not None:
        file_crud.create_file(db=db,url=form_data.file,weekday_id=query.id)

    return query


@weekday_router.put(
    "/weekdays",
    response_model=weekday_sch.WeekdaysGet,
    response_model_exclude_none=True,
)
async def update_weekdays(
    form_data: weekday_sch.WeekdaysUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return weekday_crud.update_weekday(db=db, form_data=form_data)


@weekday_router.get("/menus", response_model=Page[weekday_sch.WeekdaysMenu])
async def get_weekdays_menus(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    weekdays = weekday_crud.get_menus(db=db,id=id)
    return paginate(weekdays)



