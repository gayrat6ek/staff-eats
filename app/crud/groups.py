from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.schemas.groups import GroupsGet,GroupsCreate,GroupsUpdate
from app.models.groups import Groups



def create_group(db:Session,form_data:GroupsCreate):
    query = Groups(name=form_data.name,
                    description=form_data.description,
                    is_active=form_data.is_active,
                   )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def update_group(db:Session,form_data:GroupsUpdate):
    query = db.query(Groups).filter(Groups.id == form_data.id).first()
    if query:
        if form_data.name:
            query.name = form_data.name
        if form_data.description:
            query.description = form_data.description
        if form_data.is_active:
            query.is_active = form_data.is_active

    db.commit()
    return query


def get_groups(db:Session,id:Optional[int]=None):
    query = db.query(Groups)
    if id is not None:
        query = query.filter(Groups.id == id)
    return query.all()


def get_one_group(db:Session,id:int):
    query = db.query(Groups).filter(Groups.id==id).first()
    return query