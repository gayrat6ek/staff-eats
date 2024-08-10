from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.models.companies import Companies
from app.schemas.companies import CompaniesGet,CompaniesCreate,CompaniesUpdate


def get_companies(db:Session,name:Optional[int]=None,id:Optional[int]=None):
    query = db.query(Companies)
    if id is not None:
        query = query.filter(Companies.name.ilike(f"%{name}%"))
    return query.all()






def create_company(db:Session,form_data:CompaniesCreate):
    query = Companies(name=form_data.name,description=form_data.description,is_active=form_data.is_active)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def update_company(db:Session,form_data:CompaniesUpdate):
    query = db.query(Companies).filter(Companies.id == form_data.id).first()
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



def get_one_company(db:Session,id):
    query = db.query(Companies).filter(Companies.id==id).first()
    return query

