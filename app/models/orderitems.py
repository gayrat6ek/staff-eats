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



class Orderitems(Base):
    __tablename__ = "orderitems"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Orders", back_populates="orderitem")
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Groups", back_populates="orderitem")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())