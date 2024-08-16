from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta,date
from sqlalchemy import or_, and_, Date, cast

from uuid import UUID
from app.models.orders import Orders
from app.models.departments import Departments
from app.schemas import orders as order_sch

def create_order(db:Session,form_data:order_sch.OrderCreate):
    query = Orders(
        client_id=form_data.client_id,
        department_id=form_data.department_id,
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_orders(db:Session,id:Optional[int]=None,order_date:Optional[date]=None,company_id:Optional[int]=None,department_id:Optional[int]=None,from_date:Optional[date]=None,to_date:Optional[date]=None):
    query = db.query(Orders)
    if id is not None:
        query = query.filter(Orders.id == id)
    if order_date is not None:
        order_date -= timedelta(days=1)
        query = query.filter(Orders.created_at == order_date)
    if company_id is not None:
        query = query.filter(Departments.company_id == company_id)
    if department_id is not None:
        query = query.filter(Orders.department_id == department_id)
    if from_date is not None:
        query = query.filter(Orders.created_at >= from_date)
    if to_date is not None:
        query = query.filter(Orders.created_at <= to_date)

    return query.all()


def get_one_order(db:Session,id):
    query = db.query(Orders).filter(Orders.id==id).first()
    return query


