from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Meals(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Groups", back_populates="meal")
    price = Column(Float, nullable=True)
    is_active = Column(Integer, default=1)
    rating = relationship("Ratings", back_populates="meal")
    menu = relationship("Menus", back_populates="meal")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

