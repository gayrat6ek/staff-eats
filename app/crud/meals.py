from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.schemas.meals import GetMeals,CreateMeals,UpdateMeals
from app.models.meals import Meals



def create_meals(db:Session,form_data:CreateMeals):
    query = Meals(name=form_data.name,
                    description=form_data.description,
                    is_active=form_data.is_active,
                  group_id=form_data.group_id
                   )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_meals(db:Session,form_data:UpdateMeals):
    query = db.query(Meals).filter(Meals.id == form_data.id).first()
    if query:
        if form_data.name:
            query.name = form_data.name
        if form_data.description:
            query.description = form_data.description
        if form_data.is_active:
            query.is_active = form_data.is_active
        if form_data.group_id:
            query.group_id = form_data.group_id
    db.commit()
    return query



def get_meals(db:Session,id:Optional[int]=None,group_id:Optional[int]=None):
    query = db.query(Meals)
    if id is not None:
        query = query.filter(Meals.id == id)
    if group_id is not None:
        query = query.filter(Meals.group_id == group_id)
    return query.all()



def get_one_meal(db:Session,id):
    query = db.query(Meals).filter(Meals.id==id).first()
    return query

