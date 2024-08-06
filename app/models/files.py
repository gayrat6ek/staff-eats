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


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    weekday_id = Column(Integer, ForeignKey("weekdays.id"))
    weekday = relationship("Weekdays", back_populates="file")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="file")
    created_at = Column(DateTime, default=datetime.now(pytz.timezone("Europe/Moscow")))
    updated_at = Column(DateTime, default=datetime.now(pytz.timezone("Europe/Moscow")))

