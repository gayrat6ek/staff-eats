from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.utils.utils import hash_password
from app.schemas.users import UserGet,UserCreate,UserUpdate
from app.models.users import Users



def create_user(db:Session,form_data:UserCreate):
    query = Users(
                    password=hash_password(form_data.password),
                    is_active=form_data.is_active,
                    username=form_data.username,
                    name=form_data.name,
                    surname=form_data.surname
                   )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_user_byusername(db:Session,username:str):
    query = db.query(Users).filter(Users.username == username).first()
    return query


def get_users(db:Session,id:Optional[int]=None):
    query = db.query(Users)
    if id is not None:
        query = query.filter(Users.id == id)
    return query.all()



def update_user(db:Session,form_data:UserUpdate):
    query = db.query(Users).filter(Users.id == form_data.id).first()
    if query:
        if form_data.password is not None:
            query.password = hash_password(form_data.password)
        if form_data.is_active is not None:
            query.is_active = form_data.is_active
        if form_data.username is not None:
            query.username = form_data.username
        if form_data.name is not None:
            query.name = form_data.name
        if form_data.surname is not None:
            query.surname = form_data.surname

    db.commit()
    return query








