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
from app.crud import menus as menu_crud


weekday_router = APIRouter()


@weekday_router.get(
    "/weekdays",
    response_model=Page[weekday_sch.WeekdaysGet],
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
)
async def create_weekdays(
    form_data: weekday_sch.WeekdaysCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query =  weekday_crud.create_weekday(db=db, form_data=form_data)
    if form_data.file is not None:
        file_crud.create_file(db=db,url=form_data.file,weekday_id=query.id)

    if form_data.meals is not None:
        menu_crud.delete_menu_byweekday(db=db,id=query.id)

        for i in form_data.meals:
            menu_crud.create_menus_from_weekday(db=db,weekday_id=query.id,meal_id=i)




    return query


@weekday_router.put(
    "/weekdays",
    response_model=weekday_sch.WeekdaysGet,
)
async def update_weekdays(
    form_data: weekday_sch.WeekdaysUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    if form_data.meals is not None:
        menu_crud.delete_menu_byweekday(db=db,id=form_data.id)

        for i in form_data.meals:
            menu_crud.create_menus_from_weekday(db=db,weekday_id=form_data.id,meal_id=i)
    return weekday_crud.update_weekday(db=db, form_data=form_data)


@weekday_router.get("/menus",tags=['Menus'], response_model=Page[weekday_sch.WeekdaysMenu])
async def get_weekdays_menus(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    weekdays = weekday_crud.get_menus(db=db,id=id)
    return paginate(weekdays)


@weekday_router.get('/menus/{id}',tags=['Menus'], response_model=weekday_sch.WeekdaysMenu)
async def get_one_menu(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return weekday_crud.get_menus(db=db, id=id)


@weekday_router.get(
    "/weekdays/{id}",
    response_model=weekday_sch.WeekdaysGet,
)
async def get_one_weekday(
    id:int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return weekday_crud.get_one_weekday(db=db,id=id)





