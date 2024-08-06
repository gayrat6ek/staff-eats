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
        client_id=form_data.client_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

