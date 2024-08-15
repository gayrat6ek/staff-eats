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
from app.routes.depth import get_db, get_current_user,format_top5meal,format_meals_groups,format_meals_company
from app.schemas import users as user_sch
from app.crud import statistics as statistics_crud


statistics_router = APIRouter()


@statistics_router.get('/statistics/main', status_code=status.HTTP_200_OK)
async def get_statistics(
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    statistics_top5meal = format_top5meal(statistics_crud.overall_top_5_meals_and_ranking(db=db))
    according_to_companies = format_meals_company(statistics_crud.total_order_items_amount_today_grouped_by_company(db=db))
    according_to_meals_groups =format_meals_groups( statistics_crud.last_6_months_order_details_by_meal_group(db=db))

    return_data = {
        'top5meal': statistics_top5meal,
        'companies': according_to_companies,
        'meals_groups': according_to_meals_groups

    }


    return return_data



@statistics_router.get('/statistics/meal', status_code=status.HTTP_200_OK)
async def get_statistics(
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):


    return statistics_crud.get_meal_ratings_statistics(db=db,from_date=from_date,to_date=to_date)





