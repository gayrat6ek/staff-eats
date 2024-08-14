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
from app.crud import menus as menu_crud
from app.schemas import menus as menu_sch


menu_router = APIRouter()


@menu_router.post(
    "/menus",
    response_model=menu_sch.MenusGet,
)
async def create_menu(
    form_data: menu_sch.MenusCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return menu_crud.create_menus(db=db, form_data=form_data)


@menu_router.delete('/menus', status_code=status.HTTP_200_OK)
async def delete_menu(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return menu_crud.delete_menus(db=db, id=id)








