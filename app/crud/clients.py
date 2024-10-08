from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.schemas.clients import ClientsGet,ClientsCreate,ClientsUpdate
from app.models.clients import  Clients
from app.models.orders import Orders
from datetime import date


timezonetash = pytz.timezone('Asia/Tashkent')


def get_clients(db:Session,id:Optional[int]=None,telegram_id:Optional[str]=None):
    query = db.query(Clients).filter(Clients.is_active == 1)
    if id is not None:
        query = query.filter(Clients.id == id)
    if telegram_id is not None:
        query = query.filter(Clients.telegram_id == cast(telegram_id, String))
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
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.username is not None:
            query.username = form_data.username
        if form_data.is_active is not None:
            query.is_active = form_data.is_active
        if form_data.telegram_id is not None:
            query.telegram_id = form_data.telegram_id
        if form_data.department_id is not None:
            query.department_id = form_data.department_id
    db.commit()
    return query




def logout(db:Session,current_user):
    query = db.query(Clients).filter(Clients.telegram_id == current_user).first()
    if query:
        query.department_id = None
    db.commit()
    return query


def get_clients_without_orders_today(db: Session):
    # Get the current date
    today = datetime.now(tz=timezonetash).date()

    # Subquery to get client IDs who have placed orders today
    subquery = db.query(Orders.client_id).filter(
        cast(Orders.created_at, Date) == today
    ).distinct()

    # Query to get all active clients who have not placed an order today
    clients_without_orders_today = db.query(Clients).filter(
        Clients.is_active == 1,
        Clients.id.notin_(subquery)
    ).all()

    return clients_without_orders_today

