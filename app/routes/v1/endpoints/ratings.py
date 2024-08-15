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
from app.routes.depth import get_db, get_current_user,generate_excell_list_of_ratings
from app.schemas import users as user_sch
from app.schemas import ratings as rating_sch
from app.crud import ratings as rating_crud

rating_router = APIRouter()



@rating_router.post("/ratings", response_model=rating_sch.RatingsGet)
async def create_rating(
    form_data: rating_sch.RatingsCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    query = rating_crud.create_ratings(db=db, form_data=form_data)
    return query


@rating_router.get(
    "/ratings",
    response_model=Page[rating_sch.RatingsGet],
)
async def get_ratings(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    ratings = rating_crud.get_rankings(db=db, from_date=from_date, to_date=to_date, id=id)

    return paginate(ratings)




@rating_router.get(
    "/ratings/excell",
    tags=["excell"]
)
async def get_ratings_excell(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.UserGet = Depends(get_current_user),
):
    ratings = rating_crud.get_rankings(db=db, from_date=from_date, to_date=to_date, id=id)
    generate_excell_list_of_ratings(ratings,file_path='files/ratings.xlsx')
    return {'file_path':'files/ratings.xlsx'}



