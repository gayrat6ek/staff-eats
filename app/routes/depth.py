from app.db.session import SessionLocal
from typing import Union, Any
from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
import bcrypt
import random
import string

from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    HTTPException,
    status,
)
import smtplib
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
#from schemas import user_schema
#from queries import user_query as crud
from dotenv import load_dotenv
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.users import UserGet
from app.crud.users import get_user_byusername

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")
from app.core.config import settings
#from schemas import user_schema
#from queries import user_query as crud

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)
) -> UserGet:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        password = payload.get("password")

        if sub == "admin":
            if password != settings.admin_token_password:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        elif datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user: Union[dict[str, Any], None] = get_user_byusername(db, sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user



def format_top5meal(statistics_top5meal):
    formatted_meals = [
        (meal_name, round(float(average_rating), 1))
        for meal_name, average_rating in statistics_top5meal
    ]
    return formatted_meals


def format_meals_groups(meals_groups):
    formatted_meals_groups = {}
    for group_name, month, total_orders in meals_groups:
        if month not in formatted_meals_groups:
            formatted_meals_groups[month] = {}
        formatted_meals_groups[month][group_name] = total_orders
    return formatted_meals_groups


def format_meals_company(meals_company):
    formatted_meals_company = {}
    for company_name, total_order_items_amount in meals_company:
        formatted_meals_company[company_name] = total_order_items_amount
    return formatted_meals_company



