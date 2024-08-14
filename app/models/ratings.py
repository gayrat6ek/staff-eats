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


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, index=True)
    meal_id = Column(Integer, ForeignKey("meals.id"))
    meal = relationship("Meals", back_populates="rating")
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = relationship("Clients", back_populates="rating")
    comment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())