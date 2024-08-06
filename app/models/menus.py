from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
from app.db.base import Base
import pytz
import uuid


class Menus(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Integer, default=1)
    meal = relationship("Meals", back_populates="menu")
    meal_id = Column(Integer, ForeignKey("meals.id"))
    weekday = relationship("Weekdays", back_populates="menu")
    weekday_id = Column(Integer, ForeignKey("weekdays.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
