from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID

from app.models.orderitems import Orderitems


def create_orderitems(db:Session,order_id,meal_id,amount):
    query = Orderitems(
        order_id=order_id,
        meal_id=meal_id,
        amount=amount
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query