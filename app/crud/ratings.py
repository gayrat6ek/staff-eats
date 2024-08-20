from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID

from app.models.ratings import Ratings
from app.schemas.ratings import RatingsCreate


def create_ratings(db:Session,form_data:RatingsCreate):
    query = Ratings(
        rating=form_data.rating,
        meal_id=form_data.meal_id,
        client_id=form_data.client_id,
        comment=form_data.comment
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_rankings(db:Session,from_date, to_date,id:Optional[int]=None):
    query = db.query(Ratings)
    if id is not None:
        query = query.filter(Ratings.id == id)
    if from_date is not None:
        query = query.filter(Ratings.created_at >= from_date)
    if to_date is not None:
        query = query.filter(Ratings.created_at <= to_date)
    return query.all()

