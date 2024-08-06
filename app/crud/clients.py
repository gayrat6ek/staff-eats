from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID

from app.schemas.clients import ClientsGet,ClientsCreate,ClientsUpdate
from app.models.clients import  Clients


def get_clients(db:Session,id:Optional[int]=None):
    query = db.query(Clients).filter(Clients.is_active == 1)
    if id is not None:
        query = query.filter(Clients.id == id)
    return query.all()



def create_client(db:Session,form_data:ClientsCreate):
    query = Clients(
        name=form_data.name,
        username=form_data.username,
        is_active=form_data.is_active,
        telegram_id=form_data.telegram_id,
        department_id=form_data.department_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def update_client(db:Session,form_data:ClientsUpdate):
    query = db.query(Clients).filter(Clients.id == form_data.id).first()
    if query:
        if form_data.name:
            query.name = form_data.name
        if form_data.username:
            query.username = form_data.username
        if form_data.is_active:
            query.is_active = form_data.is_active
        if form_data.telegram_id:
            query.telegram_id = form_data.telegram_id
        if form_data.department_id:
            query.department_id = form_data.department_id
    db.commit()
    return query


