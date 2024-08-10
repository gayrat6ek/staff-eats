from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID

from app.schemas.weekdays import WeekdaysGet,WeekdaysCreate,WeekdaysUpdate
from app.models.weekdays import Weekdays


def create_weekday(db:Session,form_data:WeekdaysCreate):
    query = Weekdays(name=form_data.name,
                    description=form_data.description,
                    is_active=form_data.is_active,
                   )

    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_weekday(db:Session,form_data:WeekdaysUpdate):
    query = db.query(Weekdays).filter(Weekdays.id == form_data.id).first()
    if query:
        if form_data.name:
            query.name = form_data.name
        if form_data.description:
            query.description = form_data.description
        if form_data.is_active:
            query.is_active = form_data.is_active

    db.commit()
    db.refresh(query)
    return query


def get_weekdays(db:Session,id:Optional[int]=None):
    query = db.query(Weekdays).filter(Weekdays.is_active == 1)
    if id is not None:
        query = query.filter(Weekdays.id == id)
    return query.all()


def get_menus(db:Session,id:int):
    query = db.query(Weekdays)
    if id is not None:
        query = query.filter(Weekdays.id == id)
    return query.all()


def get_one_weekday(db:Session,id:int):
    query = db.query(Weekdays).filter(Weekdays.id==id).first()
    return query

