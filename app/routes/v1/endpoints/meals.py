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
from app.crud import meals as meal_crud
from app.schemas import meals as meal_sch


meal_router = APIRouter()


@meal_router.get(
    "/meals",
    response_model=Page[meal_sch.GetMeals],
    response_model_exclude_none=True,
)
async def get_meals(
    id: Optional[int] = None,
    group_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    meals = meal_crud.get_meals(db=db,id=id,group_id=group_id)
    return paginate(meals)


@meal_router.post(
    "/meals",
    response_model=meal_sch.GetMeals,
    response_model_exclude_none=True,
)
async def create_meal(
    form_data: meal_sch.CreateMeals,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return meal_crud.create_meals(db=db, form_data=form_data)


@meal_router.put(
    "/meals",
    response_model=meal_sch.GetMeals,
    response_model_exclude_none=True,
)
async def update_meal(
    form_data: meal_sch.UpdateMeals,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    return meal_crud.update_meals(db=db, form_data=form_data)
