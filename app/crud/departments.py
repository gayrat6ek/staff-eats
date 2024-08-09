from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.schemas.departments import DepartmentsGet,DepartmentsCreate,DepartmentsUpdate
from app.models.departments import Departments


def create_department(db:Session,form_data:DepartmentsCreate):
    query = Departments(name=form_data.name,
                        description=form_data.description,
                        company_id=form_data.company_id,
                        is_active=form_data.is_active,
                        password=form_data.password)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_department(db:Session,form_data:DepartmentsUpdate):
    query = db.query(Departments).filter(Departments.id == form_data.id).first()
    if query:
        if form_data.name:
            query.name = form_data.name
        if form_data.description:
            query.description = form_data.description
        if form_data.company_id:
            query.company_id = form_data.company_id
        if form_data.is_active:
            query.is_active = form_data.is_active
        if form_data.password:
            query.password = form_data.password

    db.commit()
    return query


def get_departments(db:Session,id:Optional[int]=None,company_id:Optional[int]=None,password:Optional[str]=None):
    query = db.query(Departments).filter(Departments.is_active == 1)
    if id is not None:
        query = query.filter(Departments.id == id)
    if company_id is not None:
        query = query.filter(Departments.company_id == company_id)
    if password is not None:
        query = query.filter(Departments.password == password)
    return query.all()


def get_one_department(db:Session,id:int):
    query = db.query(Departments).filter(Departments.id==id).first()
    return query