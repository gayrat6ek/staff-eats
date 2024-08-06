from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from app.schemas.files import FilesGet,FilesDelete
from app.models.files import  Files



def create_file(db:Session,weekday_id:Optional[int]=None,user_id:Optional[int]=None,url:Optional[str]=None):
    query = Files(weekday_id=weekday_id,user_id=user_id,url=url)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def delete_file(db:Session,form_data:FilesDelete):
    query = db.query(Files).filter(Files.id==form_data.id).delete()
    db.commit()
    return query