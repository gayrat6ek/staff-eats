from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.models.menus import Menus
from app.schemas.menus import MenusGet,MenusCreate,MenusDelete


def get_menus(db:Session,id:Optional[int]=None):
    query = db.query(Menus)
    if id is not None:
        query = query.filter(Menus.id == id)
    return query.all()


def create_menus(db:Session,form_data:MenusCreate):
    query = Menus(
        meal_id=form_data.meal_id,
        weekday_id=form_data.weekday_id,
        is_active=form_data.is_active
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def delete_menus(db:Session,id:int):
    query = db.query(Menus).filter(Menus.id == id).first()
    if query:
        db.delete(query)
    db.commit()
    return query


def delete_menu_byweekday(db:Session,id:int):
    query = db.query(Menus).filter(Menus.weekday_id == id).all()
    if query:
        for i in query:
            db.delete(i)
        db.commit()
    return query


def create_menus_from_weekday(db:Session,weekday_id:int,meal_id:int):
    query = Menus(
        meal_id=meal_id,
        weekday_id=weekday_id,
        is_active=1
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
